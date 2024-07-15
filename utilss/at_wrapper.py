'''
Author: pangay 1623253042@qq.com
Date: 2024-01-11 21:21:42
LastEditors: pangay 1623253042@qq.com
LastEditTime: 2024-01-21 23:06:58
FilePath: /Air_Taxi_simulation/utils/at_wrapper.py
'''
import numpy as np
import gymnasium as gym
#from gym import spaces
from gymnasium import spaces  #考虑不同版本
from gymnasium.core import Env
from gym.spaces import Box
from collections import deque
from typing import Any, SupportsFloat, Tuple, Dict

class atWrapper(gym.Wrapper):
    """TSC Env Wrapper for single junction with tls_id
    """
    def __init__(self, env: Env) -> None:
        super().__init__(env)


        # Dynamic Information
        self.state = None # 当前的 state
        self.action_space =  spaces.MultiBinary(4)
        self.observation_space = spaces.Box(low= 0, high = 1000, shape=(9, 4), dtype = np.int64)
        self.past_reward = 0
        # 4 个行人的位置 起点 终点 
        # 机场的位置 两个坐标 
        # 车的速度 飞机的速度 排队等待的人数  

    def state_wrapper(self, state, vehicle2person, info_wrapper):
        """构建state的格式
        """
        state_wrapper = []
        for i in state['people']: #get passenger position 
              destination = state['people'][i].get_state()
              state_wrapper.append(destination[i][0])
              state_wrapper.append(destination[i][1])
        state_wrapper = np.array(state_wrapper)
        state_wrapper = state_wrapper.reshape(4,-1) #passenger position
        uam_info_list = []
        for i in range(0,2):
            uam_info = state['UAM'][i].get_state()
        #静态信息
            uam_positon = np.array([0,0,0,0])
            uam_positon[0:2] = uam_info[0]
            uam_positon[2:] = uam_info[1]
            uam_info_list.append(uam_positon)
        #动态信息
            uam_wait = np.array([0,0,0,0])
            uam_wait[0] = uam_info[2] # wait person
            uam_wait[1] = uam_info[3] # wait time
            uam_wait[2] = uam_info[4]
            uam_wait[3] = uam_info[5]
            uam_info_list.append(uam_wait)
        uam_info_list = np.array(uam_info_list)
        #state_wrapper = np.insert(state_wrapper, 0, values=uam_positon, axis=0
        state_wrapper = np.vstack((state_wrapper,uam_info_list))
        state_wrapper = np.insert(state_wrapper, 8, values=info_wrapper, axis=0)

        return state_wrapper
    
    # 机动车匹配模型 #重新写 match 不需要提前去接，直接默认接到
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

    # action = 0,1
    def action_wrapper(self, action, vehicle2person):
        action_wrapper = {}
        i = 0 
        for people in self.state['people']:
            #[vehicle_id, if choose UAM] it can chouse 'UAM' or 'ground'
            action_wrapper[people] = [vehicle2person[i], action[i]]
            i += 1
        return action_wrapper

    def info_wrapper(self,info):
        temp_state = [0,0,0,0]
        for nam in info['persons'].person:
            if info['persons'].person[nam].state == 'v':
                vertiport_up_position =int(info['persons'].person[nam].vertiport_up_position)
                temp_state[vertiport_up_position] += 1
     
        return temp_state

    def reward_wrapper(self, reward):

        return -1 * reward
    
    def reset(self, seed=0) -> Tuple[Any, Dict[str, Any]]:
        
        state =  self.env.reset()
        self.past_reward = 0
        self.state = state
        self.vehicle2person = self.vehicle_match(state)
        info_wrapper = [0,0,0,0]
        state_wrapper = self.state_wrapper(state = state, vehicle2person = self.vehicle2person, info_wrapper = info_wrapper )
        info =  {'uam_fly_time':0, 'uam_wait_time':0, 'reward_drive_time':0,'reward_match_time':0}
        return state_wrapper, info
    

    def step(self, action: Any) -> Tuple[Any, SupportsFloat, bool, bool, Dict[str, Any]]:
        """更新路口的 state
        """
        action = self.action_wrapper(action = action, vehicle2person = self.vehicle2person)
        state, rewards, truncated, dones, info = super().step(action) # 与环境交互
        self.state = state
        self.vehicle2person = self.vehicle_match(state)
        info_wrapper = self.info_wrapper (info = info)
        state_wrapper = self.state_wrapper(state = state, vehicle2person = self.vehicle2person, info_wrapper = info_wrapper) # 处理每一帧的数据
        reward_wrapper = self.reward_wrapper(rewards)
    
        return state_wrapper, reward_wrapper, truncated, dones, info
    

    def close(self) -> None:
        return super().close()
    