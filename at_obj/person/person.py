'''
Description: 
Author: PangAY
Date: 2023-12-08 20:51:05
LastEditTime: 2023-12-10 21:16:39
LastEditors: pangay 1623253042@qq.com
'''

from loguru import logger
from typing import List, Tuple
import random

class PersonInfo(object):
    """
    描述行人的数据，包括行人ID，起始点，终点和出发时间
    """
    def __init__(self, id:str ='0', time:int =0,
                 origin_position:list[int,int] =[
                     random.randint(0, 30),
                     random.randint(0, 30)],
                 destination_position:list[int, int] =[
                     random.randint(70, 99),
                     random.randint(70, 99)]
                     )-> None: #初始化
        
        self.id = id
        self.vehicle= 0 #vehicle_id 
        self.origin_position = origin_position #起始点
        self.destination_position=destination_position#终点 在地图的位置
        self.begin_time = time #行人出发时间
        self.state='wait' #两种状态 wait， 没有匹配， drive, 匹配成功，

    
    def update_state(self, vehicle_id):
        self.state = 'drive'
        self.vehicle = vehicle_id
    def get_state(self):
        #print(f'{self.id} | origin_position {self.origin_position} | '
        #      f'destination_position {self.destination_position} | state { self.state}')
        return {self.id:[self.origin_position,
                         self.destination_position]}
    def create_object(self, id, time, ):
        self.id=id
        self.begin_time = time
        return self
