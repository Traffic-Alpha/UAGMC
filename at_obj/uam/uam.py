'''
Description: 
Author: PangAY
Date: 2023-12-08 21:14:21
LastEditTime: 2024-01-22 13:47:52
LastEditors: pangay 1623253042@qq.com
'''
import math
import numpy as np 
import random

from typing import Dict, List

from at_obj.map.map import Map

class UAM_Lane(object): 
    """
    Describe UAM route data, including starting point, end point, speed and passenger flow
    """
    def __init__(self, 
                 id: int = 0, 
                 speed: int = 4, # 120 km/h
                 volume: int = 3,
                ) -> None: #初始化
        # map information
        sim_map = Map()
        self.id = id
        self.origin_position = sim_map.vertiport_origin_position 
        self.destination_position = sim_map.vertiport_destination_position 
        self.speed = speed 
        # number of passengers that can be transported per minute
        self.volume = volume
        self.now_volume = 0
        # number of waiting people
        self.wait_person = 0 
        self.person_list = []
        # The number of people arriving at time t
        self.total_person = 0
        self.leave_person = 0
        self.time = 0
    
    def add_new_passenger(self, person: str):
        
        self.person_list.append(person)
        self.wait_person += 1

    def get_wait_time(self): #greedy 只能看到现在排队的人数
        
        return int(self.wait_person/self.volume)

    def cal_distance(self, p1: List[int], p2: List[int]): #飞行距离
        return math.sqrt(
            math.pow((p2[0] - p1[0]), 2) + 
            math.pow((p2[1] - p1[1]), 2)
            )
    
    def get_fly_time(self):
        distance = self.cal_distance(
            self.origin_position, self.destination_position)
        return int(distance/self.speed)

    def update_objects_state(self, time: int):
        
        self.time = time 
        self.now_volume = self.volume +  random.randint(-1,1)
        self.wait_person = self.wait_person - self.now_volume # 加一些随机性
        self.wait_person = max(0,self.wait_person)
    
    def get_wait_person(self):
        return self.wait_person
    
    def get_state(self):
        wait_time = self.get_wait_time()
        fly_time = self.get_fly_time()
        return(self.origin_position, 
               self.destination_position, 
               self.wait_person, fly_time, wait_time, self.now_volume) 
    
    def init_builder(self):
        self.wait_person = 0 
        self.person_list = []
        # The number of people arriving at time t
        self.time = 0

