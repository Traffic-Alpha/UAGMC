import numpy as np
import gymnasium as gym
from gymnasium import spaces

from rl_env.observation_encoder import ObservationEncoder
from rl_env.action_decoder import ActionDecoder


class UAMRLWrapper(gym.Env):
    """
    RL wrapper on top of Scenario.
    ALL RL logic stays here.
    """

    metadata = {"render.modes": []}

    def __init__(
        self,
        scenario,
        candidate_from_vertiports,
        to_vertiport,
        max_time: int = 420
    ):
        super().__init__()

        self.env = scenario
        self.max_time = max_time

        self.encoder = ObservationEncoder(
            num_vertiports=len(self.env.vertiports.vertiport_list)
        )

        self.decoder = ActionDecoder(
            candidate_from_vertiports,
            to_vertiport
        )

        # ===== Gym spaces =====
        self.observation_space = spaces.Box(
            low=0,
            high=1e6,
            shape=(self.encoder.obs_dim,),
            dtype=np.float32
        )

        self.action_space = spaces.Discrete(
            len(candidate_from_vertiports)
        )

        self.state = None

    # =====================
    # Gym API
    # =====================
    def reset(self, *, seed=None, options=None):
        self.state = self.env.reset()
        obs = self.encoder.encode(self.env, self.state)
        return obs, {}

    def step(self, action: int):

        # =========================
        # 1. Prepare action for env
        # =========================
        waiting = self.state["waiting_decisions"]

        env_action = None
        if len(waiting) > 0:
            pid = waiting[0]
            env_action = self.decoder.decode(action, pid)

        # =========================
        # 2. Single env step
        # =========================
        self.state, env_reward, terminated, truncated, info = self.env.step(env_action)

        # =========================
        # 3. Observation
        # =========================
        obs = self.encoder.encode(self.env, self.state)

        return obs, env_reward, terminated, truncated, info
