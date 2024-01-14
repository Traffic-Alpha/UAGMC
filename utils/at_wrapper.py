'''
Author: pangay 1623253042@qq.com
Date: 2024-01-11 21:21:42
LastEditors: pangay 1623253042@qq.com
LastEditTime: 2024-01-14 22:35:56
FilePath: /Air_Taxi_simulation/utils/at_wrapper.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import numpy as np
import gymnasium as gym
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
        self.observation_space = spaces.Box(low= 0, high = 1000, shape=(4, 4),dtype = np.int64)

        # 4 个行人的位置 起点 终点 
        # 机场的位置 两个坐标 
        # 车的速度 飞机的速度 排队等待的人数  

    def state_wrapper(self, state):
        """构建state的格式
        """
        print('state wrapper', state)
        p = []
        for i in state['people']: #get state
              destination = state['people'][i].get_state()
              p.append(destination[i][0])
              p.append(destination[i][1])
        p = np.array(p)
        p = p.reshape(4,-1)
        print('p',p)
        state_wrapper = p
        return state_wrapper
    
    def action_wrapper(self, action):
        action_wrapper = {}
        i = 0
        for people in self.state['people']:
            #[vehicle_id, if choose UAM] it can chouse 'UAM' or 'ground'
            action_wrapper[people] = [i,'UAM']
            i+= 1
        return action_wrapper

    def reset(self, seed=0) -> Tuple[Any, Dict[str, Any]]:
        
        state =  self.env.reset()
        self.state = state
        state_wrapper = self.state_wrapper(state = state)
        
        info = state
        return state_wrapper, info
    

    def step(self, action: Any) -> Tuple[Any, SupportsFloat, bool, bool, Dict[str, Any]]:
        """更新路口的 state
        """
        action = self.action_wrapper(action = action)
        print('actoin',action)
        state, rewards, truncated, dones, infos = super().step(action) # 与环境交互
        self.state = state
        state_wrapper = self.state_wrapper(state = state) # 处理每一帧的数据

        return state_wrapper, rewards, truncated, dones, infos
    

    def close(self) -> None:
        return super().close()
    