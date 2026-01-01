import numpy as np


class ObservationEncoder:
    """
    System-level fixed-dimension observation encoder
    (Aggregated eVTOL-aware version)
    """

    def __init__(self, num_vertiports: int):
        self.num_vertiports = num_vertiports

        # passenger: origin(x,y) + destination(x,y)
        self.person_dim = 4

        # per vertiport aggregated features: 
        # waiting_cnt + incoming_cnt + idle_evtols + charging_evtols + flying_evtols +
        # total_evtols + avg_onboard + max_onboard + avg_charge_time + avg_flight_time + available_capacity_ratio
        self.vertiport_dim = 11

        self.obs_dim = self.person_dim + num_vertiports * self.vertiport_dim

    def encode(self, env, state):
        """
        Encode current environment state into a fixed-size vector.
        If no waiting passenger, passenger part is zero-padded.
        """

        obs = []

        # ======================
        # 1. Passenger info
        # ======================
        waiting = state["waiting_decisions"]

        if len(waiting) > 0:
            pid = waiting[0]  # decision focus: first waiting passenger
            p = env.persons.persons[pid]
            obs.extend(p.origin_position)
            obs.extend(p.destination_position)
        else:
            obs.extend([0.0, 0.0, 0.0, 0.0])

        # ======================
        # 2. Vertiport info
        # ======================
        for _, v in env.vertiports.vertiport_list.items():
            
            # 当前在该 vertiport 等待的 passenger
            waiting_cnt = len(v.person_list)

            # 正在前往该 vertiport 的 passenger
            incoming_cnt = 0
            for pid, person in env.persons.persons.items():
                if person.state == "enroute" and str(person.origin_vertiport_id) == v.id:
                    incoming_cnt += 1

            idle_evtols = 0
            charging_evtols = 0
            flying_evtols = 0

            onboard_list = []
            remaining_charge_time = []
            remaining_flight_time = []

            max_capacity = 0
            used_capacity = 0

            for ev in v.evtol_list:
                s = ev.state.name

                # ---- state count ----
                if s == "IDLE":
                    idle_evtols += 1
                elif s == "CHARGING":
                    charging_evtols += 1
                elif s == "FLYING":
                    flying_evtols += 1

                # ---- capacity ----
                cap = ev.max_passenger
                cur = ev.current_passenger
                max_capacity += cap
                used_capacity += cur
                onboard_list.append(cur)

                # ---- time / energy ----
                if hasattr(ev, "remaining_charge_time"):
                    remaining_charge_time.append(ev.remaining_charge_time)

                if hasattr(ev, "remaining_flight_time"):
                    remaining_flight_time.append(ev.remaining_flight_time)

            total_evtols = len(v.evtol_list)

            # ---- aggregated stats ----
            avg_onboard = np.mean(onboard_list) if onboard_list else 0.0
            max_onboard = np.max(onboard_list) if onboard_list else 0.0

            avg_charge_time = (
                np.mean(remaining_charge_time) if remaining_charge_time else 0.0
            )
            avg_flight_time = (
                np.mean(remaining_flight_time) if remaining_flight_time else 0.0
            )

            available_capacity_ratio = (
                (max_capacity - used_capacity) / max_capacity
                if max_capacity > 0 else 0.0
            )

            obs.extend([
                float(waiting_cnt),          # 当前在该 vertiport 等待的乘客数
                float(incoming_cnt),         # 正在前往该 vertiport 的乘客数
                float(idle_evtols),
                float(charging_evtols),
                float(flying_evtols),
                float(total_evtols),
                float(avg_onboard),
                float(max_onboard),
                float(avg_charge_time),
                float(avg_flight_time),
                float(available_capacity_ratio),
            ])

        return np.array(obs, dtype=np.float32)
