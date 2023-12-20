'''
Description: 
Author: PangAY
Date: 2023-12-08 21:14:21
LastEditTime: 2023-12-20 17:48:18
LastEditors: pangay 1623253042@qq.com
'''
import math
import numpy as np 

from typing import Dict, List

from at_obj.map.map import Map

class UAM_Lane(object): 
    """
    Describe UAM route data, including starting point, end point, speed and passenger flow
    """
    def __init__(self, 
                 id: int = 0, 
                 speed: int = 10, 
                 volume: int = 2,
                ) -> None: #初始化
        # map information
        sim_map = Map()
        self.id = id
        self.origin_position = sim_map.vertiport_origin_position 
        self.destination_position = sim_map.vertiport_destination_position 
        self.speed = speed 
        # number of passengers that can be transported per minute
        self.volume = volume
        # number of waiting people
        self.wait_person = 0 
        self.person_list = []
        self.wait_list = np.zeros(1000)
        # The number of people arriving at time t
        self.time = 0
    
    def add_new_passenger(self, person: str, arrive_time: int):
        
        self.person_list.append(person)
        self.wait_list[arrive_time + self.time] += 1

    def get_wait_time(self):
        
        return int(self.wait_person/self.volume)
    
    def cal_distance(self, p1: List[int], p2: List[int]):
        return math.sqrt(
            math.pow((p2[0] - p1[0]), 2) + 
            math.pow((p2[1] - p1[1]), 2)
            )
    
    def get_fly_time(self):
        distance = self.cal_distance(
            self.origin_position, self.destination_position)
        return int(distance/self.speed)

    def update_objects_state(self, time: int):

        self.wait_person = self.wait_person + self.wait_list[time]
        self.time = time
        self.wait_person = self.wait_person - self.volume 
        self.wait_person = max(0,self.wait_person)

    def get_state(self):

        return(self.origin_position, 
               self.destination_position, 
               self.wait_person) 