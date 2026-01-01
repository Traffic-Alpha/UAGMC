import random
from typing import Dict, List, Any, Optional
from at_obj.evtol.evtol import eVTOL
from at_obj.evtol.evtol_spec import eVTOLSpec

class eVTOLBuilder:
    """
    EVTOL manager.
    Responsibilities:
    - spawning EVTOLs
    - updating dynamic states (flight, charging, idle)
    - providing status information for scheduling
    """

    def __init__(self, vertiport_ids: Optional[List[str]] = None):
        self.evtols: Dict[str, eVTOL] = {}
        self.time = 0
        self.vertiport_ids = vertiport_ids if vertiport_ids else ["0", "1"]

    def reset(self):
        """重置 EVTOL"""
        self.time = 0
        self.evtols.clear()

    def _create_evtol(self, evtol_id: str, vertiport_id: Optional[str] = None) -> eVTOL:
        """生成单架 EVTOL"""
        spec = eVTOLSpec(
            id=evtol_id,
            model=f"Model-{evtol_id}",
            manufacturer="UAM Inc.",
            capacity=random.randint(2, 4),
            max_speed=random.uniform(100, 150),
            range_km=random.uniform(50, 100),
            battery_capacity_kwh=random.uniform(50, 100),
            min_reserve_ratio=0.1,
            energy_consumption_kwh_per_km=random.uniform(0.2, 0.5),
            charge_rate_kwh_per_min=random.uniform(0.5, 1.0)
        )
        current_vertiport_id = vertiport_id if vertiport_id is not None else random.choice(self.vertiport_ids)
        return eVTOL(
            id=evtol_id,
            spec=spec,
            current_vertiport_id=current_vertiport_id
        )

    def spawn_evtol(self, evtol_id: str, vertiport_id: Optional[str] = None) -> eVTOL:
        """
        生成 EVTOL 并注册到 Builder
        """
        if evtol_id in self.evtols:
            raise ValueError(f"EVTOL id {evtol_id} 已存在！")
        evtol = self._create_evtol(evtol_id, vertiport_id)
        self.evtols[evtol_id] = evtol
        return evtol

    def spawn_replacement_evtol(self, evtol_id: str, vertiport_id: str) -> eVTOL:
        """
        生成补位 EVTOL，id 由外部提供
        """
        return self.spawn_evtol(evtol_id, vertiport_id)

    def update_objects_state(self, time: int, delta_time_min: float = 1.0):
        """推进仿真时间"""
        self.time = time
        for evtol in self.evtols.values():
            evtol.step(delta_time_min)

    def get_available_evtols(self) -> List[str]:
        """返回可用 EVTOL id 列表"""
        return [ev.id for ev in self.evtols.values() if ev.is_available()]

    def get_state(self) -> Dict[str, Dict[str, Any]]:
        """返回所有 EVTOL 状态"""
        return {
            ev.id: {
                "state": ev.state.name,
                "current_vertiport": ev.current_vertiport_id,
                "target_vertiport": ev.target_vertiport_id,
                "battery_kwh": ev.battery_kwh,
                "passenger_count": ev.passenger_ids,
                "remaining_time": ev.remaining_time
            } for ev in self.evtols.values()
        }

    def get_next_available_evtol(self, vertiport_id: str) -> Optional[eVTOL]:
        """返回指定 vertiport 的下一架可用 EVTOL"""
        candidates = [
            ev for ev in self.evtols.values()
            if ev.current_vertiport_id == vertiport_id and ev.is_available()
        ]
        if not candidates:
            return None
        candidates.sort(key=lambda x: x.battery_kwh, reverse=True)
        return candidates[0]
