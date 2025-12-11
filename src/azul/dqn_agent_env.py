import random
import math
from collections import deque, namedtuple
from typing import Tuple, List

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

import azul
from azul.table import Table
from azul.player import Player
from azul.color import Color

try:
    from azul.color import Color as AZ_COLOR
    COLORS = list(AZ_COLOR)
    NUM_COLORS_DEFAULT = len(COLORS)
except Exception:
    AZ_COLOR = None
    COLORS = []
    NUM_COLORS_DEFAULT = 5

# hyperparams
GAMMA = 0.99
LR = 1e-4
BATCH_SIZE = 64
REPLAY_SIZE = 100000
MIN_REPLAY = 512
TARGET_UPDATE_FREQ = 1000
EPS_START = 1.0
EPS_END = 0.05
EPS_DECAY = 20000
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

Transition = namedtuple("Transition", ("s", "a", "r", "s2", "done"))


def to_tensor(x, dtype=torch.float32):
    return torch.tensor(x, dtype=dtype, device=DEVICE)


class QNetwork(nn.Module):
    def __init__(self, input_dim: int, output_dim: int):
        super().__init__()
        hidden = 512
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, output_dim),
        )

    def forward(self, x):
        return self.net(x)


class ReplayBuffer:
    def __init__(self, capacity: int):
        self.buf = deque(maxlen=capacity)

    def push(self, *args):
        self.buf.append(Transition(*args))

    def sample(self, batch_size: int):
        batch = random.sample(self.buf, batch_size)
        return Transition(*zip(*batch))

    def __len__(self):
        return len(self.buf)


class AzulEnv:
    # - table.factories
    # - table.center
    # - Supplier.supplier_id
    # - Factory.tiles, Center.tiles
    # - wall.lines
    # - PatternLine.slots, Slot.color, Slot.is_empty
    # - FloorLine.slots
    # - Player.board.wall.place_tile

    def __init__(self, az_game, agent_player_index: int = 0, num_players=2):
        super().__init__()
        self.num_players = num_players
        self.table = Table(num_players)
        self.players = [Player(f"Player {i}") for i in range(num_players)]
        self.current_player = 0
        self.game = az_game
        self.agent_idx = agent_player_index

        self.table = self.game.table
        self.factories = self.table.factories
        self.center = self.table.center

        self.num_factories = len(self.factories)
        self.num_suppliers = self.num_factories + 1  # factories + center

        self.ColorEnum = Color
        self.colors = list(Color)
        self.num_colors = len(self.colors)

        self.pattern_lines = 5
        self.action_target_options = self.pattern_lines + 1  # floor line
        self.action_size = self.num_suppliers * self.num_colors * self.action_target_options

        self._prev_points = None

    def _color_to_index(self, color):
        """Convert Color or None to index."""
        if color is None:
            return None
        return self.colors.index(color)

    def _encode_suppliers(self):
        C = self.num_colors
        # For each supplier: count of each color, plus 1 "other" column
        mat = np.zeros((self.num_suppliers, C + 1), dtype=np.float32)

        # Factories
        for i, f in enumerate(self.factories):
            for tile in f.tiles:
                idx = self._color_to_index(tile.color)
                if idx is None:
                    mat[i, C] += 1
                else:
                    mat[i, idx] += 1

        # Center
        for tile in self.center.tiles:
            idx = self._color_to_index(tile.color)
            if idx is None:
                mat[-1, C] += 1
            else:
                mat[-1, idx] += 1

        return mat.flatten()

    def _encode_player_board(self, player):
        C = self.num_colors

        pattern_parts = []
        for i, pl in enumerate(player.board.pattern_lines):
            slots = pl.slots
            total = len(slots)
            filled = sum(0 if s.is_empty() else 1 for s in slots)
            frac = filled / total

            # determine fixed color for pattern line
            color_idx = None
            for s in slots:
                if s.color is not None:
                    color_idx = self._color_to_index(s.color)
                    if color_idx is not None:
                        break

            onehot = np.zeros(C, dtype=np.float32)
            if color_idx is not None:
                onehot[color_idx] = 1.0

            pattern_parts.append(np.concatenate(([frac], onehot)))

        pattern_vec = np.concatenate(pattern_parts)

        wall_occ = np.zeros(25, dtype=np.float32)
        lines = player.board.wall.lines  #list[list[Slot]]

        for r in range(5):
            for c in range(5):
                if not lines[r][c].is_empty():
                    wall_occ[r * 5 + c] = 1.0

        floor = player.board.floor_line
        slots = floor.slots
        Ccount = np.zeros(C, dtype=np.float32)
        filled = 0
        for sl in slots:
            if not sl.is_empty():
                filled += 1
                t = sl.tile
                idx = self._color_to_index(t.color)
                if idx is not None:
                    Ccount[idx] += 1

        floor_vec = np.concatenate(([filled / len(slots)], Ccount / len(slots)))

        score_vec = np.array([player.points / 100], dtype=np.float32)

        return np.concatenate([pattern_vec, wall_occ, floor_vec, score_vec])

    def encode_state(self):
        sup = self._encode_suppliers()
        agent = self._encode_player_board(self.game.players[self.agent_idx])

        opp_parts = []
        for i, p in enumerate(self.game.players):
            if i == self.agent_idx:
                continue
            frac = 0
            for j, pl in enumerate(p.board.pattern_lines):
                slots = pl.slots
                filled = sum(0 if s.is_empty() else 1 for s in slots)
                frac += filled / len(slots)
            opp_parts.append(np.array([p.points / 100, frac / 5], dtype=np.float32))

        opp_vec = np.concatenate(opp_parts) if opp_parts else np.zeros(2, dtype=np.float32)

        return np.concatenate([sup, agent, opp_vec]).astype(np.float32)

    def _decode_action(self, idx):
        per_supplier = self.num_colors * self.action_target_options
        supplier = idx // per_supplier
        rem = idx % per_supplier
        color = rem // self.action_target_options
        target = rem % self.action_target_options
        return supplier, color, target

    def _encode_action(self, s, c, t):
        return s * self.num_colors * self.action_target_options + c * self.action_target_options + t

    def legal_action_mask(self):
        mask = np.zeros(self.action_size, dtype=bool)

        for a in range(self.action_size):
            s_id, c_id, target = self._decode_action(a)

            supplier = self.factories[s_id] if s_id < self.num_factories else self.center

            contains_color = any(
                self._color_to_index(t.color) == c_id
                for t in supplier.tiles
            )
            if not contains_color:
                continue

            if target == self.pattern_lines:
                mask[a] = True
                continue

            player = self.game.players[self.agent_idx]
            pl = player.board.pattern_lines[target]

            if pl.is_complete():
                continue

            row = target
            color_enum = self.colors[c_id]
            wall = player.board.wall.lines

            forbidden = any(
                (slot.color == color_enum and not slot.is_empty())
                for slot in wall[row]
            )
            if forbidden:
                continue

            mask[a] = True

        return mask

    def reset(self):
        self.players = [azul.Player(f"Player {i}") for i in range(self.num_players)]
        self.game = azul.Game(self.players)
        self.table = self.game.table

        self.done = False
        self.turn_count = 0
        return self.encode_state()

    def step(self, action):
        s_id, c_id, target = self._decode_action(action)
        color_enum = self.colors[c_id]
        pattern_line = -1 if target == self.pattern_lines else target

        prev = self.game.players[self.agent_idx].points

        #execute next action
        self.game.take_turn(s_id, color_enum, pattern_line)

        now = self.game.players[self.agent_idx].points
        reward = now - prev

        done = self.game._check_end()
        print("CHECK END", done)
        next_state = self.encode_state()
        return next_state, reward, done, {}


class DQNAgent:
    def __init__(self, obs_dim: int, action_dim: int):
        self.obs_dim = obs_dim
        self.action_dim = action_dim

        self.policy_net = QNetwork(obs_dim, action_dim).to(DEVICE)
        self.target_net = QNetwork(obs_dim, action_dim).to(DEVICE)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=LR)
        self.replay = ReplayBuffer(REPLAY_SIZE)

        self.steps_done = 0

    def select_action(self, state: np.ndarray, legal_mask: np.ndarray, eval_mode=False):
        eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(-1.0 * self.steps_done / EPS_DECAY)
        self.steps_done += 1
        if eval_mode or random.random() > eps_threshold:
            with torch.no_grad():
                s_t = to_tensor(state).unsqueeze(0)
                qvals = self.policy_net(s_t).cpu().numpy().flatten()
                qvals[~legal_mask] = -1e9
                action = int(np.argmax(qvals))
                return action
        else:
            legal_indices = np.nonzero(legal_mask)[0]
            if len(legal_indices) == 0:
                return random.randrange(self.action_dim)
            return int(np.random.choice(legal_indices))

    def store_transition(self, *args):
        self.replay.push(*args)

    def optimize(self):
        if len(self.replay) < max(MIN_REPLAY, BATCH_SIZE):
            return
        trans = self.replay.sample(BATCH_SIZE)
        s = torch.tensor(np.stack(trans.s), dtype=torch.float32, device=DEVICE)
        a = torch.tensor(trans.a, dtype=torch.long, device=DEVICE).unsqueeze(1)
        r = torch.tensor(trans.r, dtype=torch.float32, device=DEVICE).unsqueeze(1)
        s2 = torch.tensor(np.stack(trans.s2), dtype=torch.float32, device=DEVICE)
        done = torch.tensor(trans.done, dtype=torch.float32, device=DEVICE).unsqueeze(1)

        q_values = self.policy_net(s).gather(1, a)
        with torch.no_grad():
            next_q = self.target_net(s2).max(1, keepdim=True)[0]
            target = r + (1.0 - done) * GAMMA * next_q

        loss = nn.functional.mse_loss(q_values, target)
        self.optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(self.policy_net.parameters(), 10.0)
        self.optimizer.step()

    def update_target(self):
        self.target_net.load_state_dict(self.policy_net.state_dict())


def train(env: AzulEnv, agent: DQNAgent, num_episodes: int = 1000):
    total_steps = 0
    for ep in range(num_episodes):
        obs = env.reset()
        done = False
        ep_reward = 0.0
        while not done:
            print("STEP BEGIN")
            mask = env.legal_action_mask()
            print("MASK OK")
            action = agent.select_action(obs, mask)
            print("ACTION =", action)
            obs2, reward, done, info = env.step(action)
            print("STEP DONE | reward=", reward, " done=", done)
            agent.store_transition(obs, action, reward, obs2, done)
            print("STORE OK")
            agent.optimize()
            print("OPTIMIZE OK")
            obs = obs2
            ep_reward += reward
            total_steps += 1
            if total_steps % TARGET_UPDATE_FREQ == 0:
                agent.update_target()
        print(f"[Episode {ep}] reward={ep_reward:.2f}")


if __name__ == "__main__":
    import azul as az

    p1 = az.Player("A")
    p2 = az.Player("B")
    game = az.Game([p1, p2])
    env = AzulEnv(game, agent_player_index=0)
    obs_dim = env.encode_state().shape[0]
    act_dim = env.action_size
    agent = DQNAgent(obs_dim, act_dim)

    train(env, agent, num_episodes=5)
