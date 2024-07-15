'''
Author: PangAY
Date: 2023-12-08 17:01:38
LastEditTime: 2024-01-22 13:55:14
LastEditors: pangay 1623253042@qq.com
'''
import sys
from pathlib import Path

parent_directory = Path(__file__).resolve().parent.parent
if str(parent_directory) not in sys.path:
    sys.path.insert(0, str(parent_directory))

import gym
from gymnasium import spaces 
#from gym import spaces
import pygame
import numpy as np
  
from at_obj.person.person_builder import PersonBuilder
from at_obj.vehicle.vehicle_builder import VehicleBuilder
from at_obj.vertiport.vertiport_builder import UamBuilder

class Scenario(gym.Env):
    def __init__(self) -> None:

        self.action_space =  spaces.MultiBinary(4)
        self.observation_space = spaces.Box(low= 0, high = 1000, shape=(9, 4),dtype = np.int64)

        self.render_mode = None
        self.time = 0 # simulate time
        self.persons = PersonBuilder(person_num = 4) # passenger list
        self.vehicles = VehicleBuilder() # vehicles builder 
        self.uam = UamBuilder() #uam 信息
        self.person_num = 0
        self.ground_num = 0 
        self.UAM_num = 0 
        self.total_traval_time = 0
        self.item = {
            'vehicle': self.vehicles,
            'people':  self.persons,
            'UAM': self.uam,
        }
        self.state = {obj_id: self.item[obj_id].get_state() for obj_id in self.item}
    def _get_obs(self):


        return {"agent": self._agent_location}
    
    def _get_info(self, state):

        return state
    
    def reset(self, seed=0):
        self.time = 0
        self.person_num = 0
        self.ground_num = 0 
        self.UAM_num = 0  #uam 的人的数量
        self.total_traval_time = 0
        self.persons.__init__()
        self.vehicles.__init__()
        self.uam.__init__()
        state = {obj_id: self.item[obj_id].get_state() for obj_id in self.item}
        #info = self._get_info()
        return state
    
    def step(self, action):
        self.time += 1
        # get passenger list
        person_list=[id for id  in self.persons.person_new] #新进来的人 决策的人
        vehicle_list=[id for id in self.vehicles.vehicles]
        # Time consuming for matching passengers and vehicles
        info = []
        # Update states and calculate reward
        # 每步 更新仿真
        #每个人都需要处理
        for person in person_list:
            # 此问题不考虑车的匹配 # taxi 的匹配

            # passenger choose lane
            vertiport_id = action[person][1]
            self.persons.person_new[person].method = 'UAM'
            self.persons.person_new[person].state = 'v'  #匹配上车
            self.persons.person_new[person].vertiport_up_position = vertiport_id # vertiport 有三个，编号为 0，1，2
            self.persons.person_new[person].vertiport_off_position = 2 # 固定降落的 vertiport 编号为 2
            
            # 计算 起点到机场起飞的时间
            self.persons.person_new[person].uam_drive_traval = self.vehicles.vehicles[  
                vehicle_list[action[person][0]]].get_drive_time(
                self.uam.vertiport_list[self.persons.person_new[person].vertiport_up_position].vertiport_position,
                self.persons.person_new[person].origin_position,
                )

            #计算 降落点到终点的时间
            self.persons.person_new[person].destination_drive_traval = self.vehicles.vehicles[
                vehicle_list[action[person][0]]].get_drive_time(
                self.uam.vertiport_list[self.persons.person_new[person].vertiport_off_position].vertiport_position, #降落机场的位置
                self.persons.person_new[person].destination_position
                )

        state = {obj_id: self.item[obj_id].get_state() for obj_id in self.item} #get state
        for nam in self.persons.person:
            if(self.persons.person[nam].state == 'arrive'):
                vertiport_up_position = self.persons.person[nam].vertiport_up_position
                self.uam.vertiport_list[vertiport_up_position].add_new_passenger(nam) #到达指定机场
                self.persons.person[nam].state = 'w'
                self.persons.person[nam].uam_wait_time = self.uam.vertiport_list[vertiport_up_position].get_wait_time()
                self.persons.person[nam].fly_time = self.uam.vertiport_list[vertiport_up_position].get_fly_time()
        
        self.uam.update_objects_state(self.time) #进行修改
        self.vehicles.update_objects_state(self.time)
        self.persons.update_objects_state(self.time)     
        wait_person = self.uam.wait_person
        reward = 0
        person_state = [] 
        for nam in self.persons.person:
            person_state.append(self.persons.person[nam].state)
            if(self.persons.person[nam].state == 'd'):
                self.person_num += 1
                self.total_traval_time += (self.time - self.persons.person[nam].begin_time)
                self.persons.person[nam].state = 'del'
        if self.person_num != 0 :
            reward = self.total_traval_time/self.person_num # 返回平均收益 
        info = {
            'wait_person':wait_person,
            'person_state':person_state,
            'persons':self.persons,
            }
        terminated = False
        dones = False
        if self.time >= 600: #终止条件
            dones = True
        return state, reward, terminated, dones, info
    
    def render(self):
        pass