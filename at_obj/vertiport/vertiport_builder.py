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
from at_obj.vertiport.vertiport import VertiportInfo


class UamBuilder(object): 
    """
    Describe UAM route data, including starting point, end point, speed and passenger flow
    """
    def __init__(self) -> None: #初始化
        # map information
        self.map = Map()
        self.vertiport_position = self.map.vertiport_station 
        # number of waiting people
        self.wait_person = 0 
        self.person_list = []
        # The number of people arriving at time t
        self.total_person = 0
        self.leave_person = 0
        self.time = 0

        self.vertiport_list:Dict[str,VertiportInfo] = {}

        self.vertiport_num = self.map.vertiport_station_num
        for num in range(0, self.vertiport_num): #
            vertiport_id =  num
            self.create_objects(vertiport_id)
        
    def create_objects(self, vertiport_id:str)->None:
        vertiport_position = self.map.vertiport_station[vertiport_id]

        vertiport_info = VertiportInfo(
            id = vertiport_id, 
            vertiport_position = vertiport_position,
        )
        
        self.vertiport_list[vertiport_id] = vertiport_info
    
    def add_new_passenger(self, person: str, vertiport_id: int):
        
        self.self.vertiport[vertiport_id].person_list.append(person)
        self.self.vertiport[vertiport_id].wait_person += 1

    def cal_distance(self, p1: List[int], p2: List[int]): #飞行距离
        return math.sqrt(
            math.pow((p2[0] - p1[0]), 2) + 
            math.pow((p2[1] - p1[1]), 2)
            )
    
    def get_fly_time(self,origin_position,destination_position, vertiport_id: int):
        distance = self.cal_distance(
            origin_position , destination_position)
        return int(distance/self.vertiport[vertiport_id].speed)

    def update_objects_state(self, time: int):
        volume_list = [1, 4]
        self.time = time
        for vertiport_id in range(0,2): #只有两机场承担起飞任务
            self.vertiport_list[vertiport_id].volume = volume_list[vertiport_id]
            self.vertiport_list[vertiport_id].now_volume = self.vertiport_list[vertiport_id].volume
            self.vertiport_list[vertiport_id].wait_person = self.vertiport_list[vertiport_id].wait_person - self.vertiport_list[vertiport_id].now_volume 
            self.vertiport_list[vertiport_id].wait_person = max(0,self.vertiport_list[vertiport_id].wait_person)
    
    #获得每个机场现在排队等待的人数
    def get_all_wait_person(self):
        wait_person_list = []
        for uam in self.vertiport_list:
            wait_person_list.append(self.vertiport_list[vertiport_id].wait_person)
        return wait_person_list

    def get_wait_person(self, vertiport_id: int):
        return self.vertiport[vertiport_id].wait_person
    
    def get_state(self):

        return(self.vertiport_list) 
    
    def init_builder(self):
        self.wait_person = 0 
        self.person_list = []
        # The number of people arriving at time t
        self.time = 0

