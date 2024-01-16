'''
Author: PangAY
Date: 2023-12-08 17:01:38
LastEditTime: 2024-01-16 20:35:10
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
from at_obj.uam.uam import UAM_Lane

class Scenario(gym.Env):
    def __init__(self) -> None:
        
        self.time = 0 # simulate time
        self.persons = PersonBuilder(person_num = 4) # passenger list
        self.vehicles = VehicleBuilder() # vehicles builder 

        self.uam=UAM_Lane()
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
        self.persons.update_objects_state(self.time)
        self.vehicles.update_objects_state(self.time)
        state = {obj_id: self.item[obj_id].get_state() for obj_id in self.item}
        #info = self._get_info()
        return state
    
    def step(self, action):
        self.time += 1
        # get passenger list
        person_list=[id for id  in self.persons.person] 
        vehicle_list=[id for id in self.vehicles.vehicles]
        # Time consuming for matching passengers and vehicles
        reward_match_time = 0 
        uam_wait_time = 0
        uam_fly_time = 0
        reward_drive_time = 0
        person_uam = 0
        person_ground = 0
        info = []
        # Update states and calculate reward
        for person in person_list:
            # match
            self.vehicles.vehicles[vehicle_list[action[person][0]]].update_state(person)
            self.persons.person[person].update_state(
                vehicle_list[action[person][0]]) 
            # The time it takes for a matching taxi to pick up passenger
            reward_match_time = reward_match_time + self.vehicles.vehicles[
                vehicle_list[action[person][0]]].get_drive_time(
                self.vehicles.vehicles[vehicle_list[action[person][0]]].origin_position,
                self.persons.person[person].origin_position)
            arrive_uam_time = self.vehicles.vehicles[
                vehicle_list[action[person][0]]].get_drive_time(
                self.uam.origin_position,
                self.persons.person[person].origin_position
                )
            # passenger choose UAM or ground
            if action[person][1] == 'UAM':
                person_uam += 1
                self.uam.add_new_passenger(self.persons.person[person], int(arrive_uam_time))
                # Queuing time
                wait_time = self.uam.get_wait_time()
                # Flying time
                fly_time = self.uam.get_fly_time()
                uam_wait_time = uam_wait_time + wait_time # 此处的 uam_wait_time 是每次观测乘坐UAM的乘客的的等待数量的总和
                uam_fly_time = uam_fly_time + fly_time
                reward_drive_time += self.vehicles.vehicles[
                vehicle_list[action[person][0]]].get_drive_time(
                     self.uam.destination_position,
                     self.persons.person[person].destination_position,
                     ) 
                
            elif action[person][1] == 'ground':
                person_ground += 1 
                reward_drive_time += self.vehicles.vehicles[
                vehicle_list[action[person][0]]].get_drive_time(
                     self.persons.person[person].origin_position,
                     self.persons.person[person].destination_position,
                     ) 
        reward = {}
        reward['reward_match_time'] = reward_match_time
        reward['reward_uam_time'] = uam_fly_time + uam_wait_time
        reward['reward_drive_time'] = reward_drive_time
        reward = uam_fly_time + uam_wait_time + reward_drive_time + reward_match_time
        state = {obj_id: self.item[obj_id].get_state() for obj_id in self.item} #get state
        self.uam.update_objects_state(self.time)
        self.vehicles.update_objects_state(self.time)
        self.persons.update_objects_state(self.time)
        wait_person = self.uam.get_wait_person()
        info = {
            'uam_fly_time':uam_fly_time, 
            'uam_wait_time':uam_wait_time, 
            'reward_drive_time':reward_drive_time,
            'reward_match_time':reward_match_time,
            'wait_person':wait_person,
            'person_uam':person_uam,
            'person_ground':person_ground,
            }
        terminated = False
        dones = False
        if self.time >= 100: #终止条件
            dones = True
        return state, reward, terminated, dones, info