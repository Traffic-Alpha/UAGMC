'''
Author: pangay 1623253042@qq.com
Date: 2024-01-11 21:21:42
LastEditors: pangay 1623253042@qq.com
LastEditTime: 2024-01-16 20:21:26
FilePath: /Air_Taxi_simulation/utils/at_wrapper.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import numpy as np
import gymnasium as gym
import copy
from gymnasium import spaces
from gymnasium.core import Env
from collections import deque
from typing import Any, SupportsFloat, Tuple, Dict

class atWrapper(gym.Wrapper):
    """TSC Env Wrapper for single junction with tls_id
    """
    def __init__(self, env: Env) -> None:
        super().__init__(env)


        # Dynamic Information
        self.state = None # 当前的 state
        self.action_space =  spaces.Box(low = np.zeros((4, ), dtype = int), high = np.array([1]*4), shape = (4, ), dtype = np.uint8) # action space 
        self.observation_space = spaces.Box(low= 0, high = 1000, shape=(6, 4),dtype = np.int64)
        # 4 个行人的位置 起点 终点 
        # 机场的位置 两个坐标 
        # 车的速度 飞机的速度 排队等待的人数  

    def state_wrapper(self, state, vehicle2person):
        """构建state的格式
        """
        state_wrapper = []
        for i in state['people']: #get passenger position 
              destination = state['people'][i].get_state()
              state_wrapper.append(destination[i][0])
              state_wrapper.append(destination[i][1])
        state_wrapper = np.array(state_wrapper)
        state_wrapper = state_wrapper.reshape(4,-1) #passenger position
        uam_info = state['UAM']
        # 静态信息
        uam_positon = np.array([0,0,0,0])
        uam_positon[0:2] = uam_info[0]
        uam_positon[2:] = uam_info[1]
        #动态信息
        uam_wait = np.array([0,0,0,0])
        uam_wait[0] = uam_info[2]
        uam_wait[1] = uam_info[3]
        uam_wait[2] = uam_info[4]
        state_wrapper = np.insert(state_wrapper, 0, values=uam_positon, axis=0)
        state_wrapper = np.insert(state_wrapper, 0, values=uam_wait, axis=0)
        
        return state_wrapper
    
    # 机动车匹配模型
    def vehicle_match(self, state):
        
        vehicle2person = []
        for i in state['people']: 
            distance_list = []
            vehicle_list = []
            for j in state['vehicle']:
                distance = state['vehicle'][j].get_drive_time(
                      state['vehicle'][j].origin_position,
                      state['people'][i].origin_position
                      )
                distance_list.append(distance)
                vehicle_list.append(j)
             #加入容错机制 防止一辆车匹配到两个人
            temp = sorted(range(len(distance_list)),key=lambda k: distance_list[k])
            vehicle_id = temp[0]
            count = vehicle2person.count(vehicle_id)
            k = 0
            while count != 0:
                k += 1
                vehicle_id = temp[k]
                count = vehicle2person.count(vehicle_id)
            vehicle2person.append(vehicle_id)

        return vehicle2person
    def action_wrapper(self, action, vehicle2person):
        action_wrapper = {}
        i = 0
        for people in self.state['people']:
            #[vehicle_id, if choose UAM] it can chouse 'UAM' or 'ground'
            if action[i] == 0:
                action_wrapper[people] = [vehicle2person[i],'ground']
            else:
                action_wrapper[people] = [vehicle2person[i],'UAM']
            i+= 1
        return action_wrapper

    def reset(self, seed=0) -> Tuple[Any, Dict[str, Any]]:
        
        state =  self.env.reset()
        self.state = state
        self.vehicle2person = self.vehicle_match(state)
        state_wrapper = self.state_wrapper(state = state, vehicle2person = self.vehicle2person)
        info =  {'uam_fly_time':0, 'uam_wait_time':0, 'reward_drive_time':0,'reward_match_time':0}
        return state_wrapper, info
    

    def step(self, action: Any) -> Tuple[Any, SupportsFloat, bool, bool, Dict[str, Any]]:
        """更新路口的 state
        """
        action = self.action_wrapper(action = action, vehicle2person = self.vehicle2person)
        state, rewards, truncated, dones, info = super().step(action) # 与环境交互
        self.state = state
        self.vehicle2person = self.vehicle_match(state)
        state_wrapper = self.state_wrapper(state = state, vehicle2person = self.vehicle2person) # 处理每一帧的数据

        return state_wrapper, rewards, truncated, dones, info
    

    def close(self) -> None:
        return super().close()
    