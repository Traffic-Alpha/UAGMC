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
from gym import spaces
import pygame
import numpy as np
  
from at_obj.person.person_builder import PersonBuilder
from at_obj.vehicle.vehicle_builder import VehicleBuilder
from at_obj.vertiport.vertiport_builder import UamBuilder

class Scenario(gym.Env):
    def __init__(self) -> None:
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
    
    def reset(self):
        self.time = 0
        self.person_num = 0
        self.ground_num = 0 
        self.UAM_num = 0 
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
        person_list=[id for id  in self.persons.person_new] 
        vehicle_list=[id for id in self.vehicles.vehicles]
        # Time consuming for matching passengers and vehicles
        info = []
        # Update states and calculate reward
        # 每步 更新仿真
        reward_match_time = 0
        for person in person_list:
            # match
            self.vehicles.vehicles[vehicle_list[action[person][0]]].update_state(person)
            self.persons.person_new[person].match_vehicle(
                 self.vehicles.vehicles[vehicle_list[action[person][0]]])#重新写 state 更新
            # The time it takes for a matching taxi to pick up passenger
            reward_match_time = reward_match_time + self.vehicles.vehicles[
                vehicle_list[action[person][0]]].get_drive_time(
                self.vehicles.vehicles[vehicle_list[action[person][0]]].origin_position,
                self.persons.person_new[person].origin_position)
            
            # passenger choose UAM or ground
            if action[person][1] == 'UAM':
                self.UAM_num += 1
                self.persons.person_new[person].method = 'UAM'
                self.persons.person_new[person].uam_drive_traval = self.vehicles.vehicles[
                vehicle_list[action[person][0]]].get_drive_time(
                self.uam.origin_position,
                self.persons.person_new[person].origin_position
                )
                self.persons.person_new[person].destination_drive_traval = self.vehicles.vehicles[
                vehicle_list[action[person][0]]].get_drive_time(
                self.uam.destination_position,
                self.persons.person_new[person].destination_position
                )
            elif action[person][1] == 'ground':
                self.ground_num += 1
                self.persons.person_new[person].method = 'ground'
                self.persons.person_new[person].ground_drive_traval = self.vehicles.vehicles[
                vehicle_list[action[person][0]]].get_drive_time(
                self.persons.person_new[person].destination_position,
                self.persons.person_new[person].origin_position
                )

        state = {obj_id: self.item[obj_id].get_state() for obj_id in self.item} #get state
        for nam in self.persons.person:
            if(self.persons.person[nam].state == 'arrive'):
                self.uam.add_new_passenger(nam)
                self.persons.person[nam].state = 'w'
                self.persons.person[nam].uam_wait_time = self.uam.get_wait_time()
                self.persons.person[nam].fly_time = self.uam.get_fly_time()
        
        self.uam.update_objects_state(self.time)
        self.vehicles.update_objects_state(self.time)
        self.persons.update_objects_state(self.time)     
        wait_person = self.uam.get_wait_person()
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
            'person_state':person_state
            }
        terminated = False
        dones = False
        if self.time >= 120: #终止条件
            print('UAM',self.UAM_num)
            print('ground',self.ground_num)
            dones = True
        return state, reward, terminated, dones, info
    
    def render(self):
        pass