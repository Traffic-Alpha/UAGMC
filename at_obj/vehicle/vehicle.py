'''
Description: 
Author: PangAY
Date: 2023-12-08 21:13:26
LastEditTime: 2023-12-08 23:27:30
LastEditors:  
'''
from typing import Dict, Any
from loguru import logger
from typing import List, Tuple
import random

class Vehicle(object):
    """
    描述机动车的数据，包括机动车ID，起始点， 和速度
    """
    def __init__(self,id:str ='0') -> None: #初始化
        
        self.id = id
        self.origin_position = [random.randint(0, 30),random.randint(0, 30)] #起始点
        self.speed= 1 #每分钟可以走1个格子
        self.passenger=None # 乘客的ID
        self.state='wait' #两种状态 wait， 没有匹配， drive, 匹配成功，

    def update_state(self, Person):
        self.state='drive'
        self.passenger=Person # 乘客ID
    
    def get_drive_time(self,position):
        travel_time=(abs(position[0]-self.origin_position[0])+abs(position[1]-self.origin_position[1]))/self.speed
        return travel_time

    def get_state(self):
        print(f'{self.id} | origin_position {self.origin_position} | state {self.state}')
        return()
    
    def create_object(self):
        
        return self