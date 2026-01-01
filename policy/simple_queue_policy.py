"""
Author: PangAY
Minimal Queue-aware Vertiport Selection Policy
Only considers the current number of waiting passengers at each vertiport.
"""

from typing import Dict, Any, List
import random


class SimpleQueueVertiportPolicy:
    def __init__(
        self,
        candidate_from_vertiports: List[int],
        to_vertiport: int,
        greedy_prob: float = 1.0
    ):
        """
        Args:
            candidate_from_vertiports: 可选起飞 vertiport
            to_vertiport: 固定目的 vertiport
            greedy_prob: 选择最优的概率
        """
        self.from_candidates = candidate_from_vertiports
        self.to_vertiport = to_vertiport
        self.greedy_prob = greedy_prob

    # =========================
    # Main interface
    # =========================
    def act(self, env, state) -> Dict[str, Dict[str, Any]]:
        """
        Return action dict for all waiting passengers
        """
        actions = {}

        for pid in state["waiting_decisions"]:
            from_vid = self._select_vertiport(env, pid)
            actions[pid] = {
                "mode": "UAM",
                "from_vertiport": from_vid,
                "to_vertiport": self.to_vertiport,
            }

        return actions

    # =========================
    # Core logic
    # =========================
    def _select_vertiport(self, env, person_id: str) -> int:
        """
        Choose the vertiport with minimal number of currently waiting passengers
        """
        # exploration
        if random.random() > self.greedy_prob:
            return random.choice(self.from_candidates)

        best_vid = None
        min_queue = float("inf")

        for vid in self.from_candidates:
            vertiport = env.vertiports.vertiport_list[str(vid)]
            queue_len = len(vertiport.person_list)  # 当前等待的人数

            if queue_len < min_queue:
                min_queue = queue_len
                best_vid = vid

        return best_vid
