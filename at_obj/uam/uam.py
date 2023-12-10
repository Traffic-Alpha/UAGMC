'''
Description: 
Author: PangAY
Date: 2023-12-08 21:14:21
LastEditTime: 2023-12-10 21:19:28
LastEditors: pangay 1623253042@qq.com
'''

from loguru import logger
from typing import List, Tuple

from at_obj.map.map import Map

class UAM_Lane(object): #空中通行的航线
    """
    描述UAM 航线数据，包括 起始点，终点， 速度和客流量
    """
    def __init__(self, id:int =0, origin_position:List[int] =[30,30], 
                 destination_position:List[int] =[70,70],
                speed:int =10, volume:int =2,
                ) -> None: #初始化
        
        sim_map = Map()
        self.id = id
        self.origin_position = sim_map.vertiport_origin_position #起始点
        self.destination_position=sim_map.vertiport_destination_position #降落点距离
        self.speed = speed #每分钟可以走10个格子
        self.volume = volume #通行数量每分钟最大通行人数
        self.wait_person = 0 #等待的人数
    
    def add_new_passenger(self, person):
        self.wait_person += 1

    def get_wait_time(self):
        
        return int(self.wait_person/self.volume)
    
    def update_state(self):
        self.wait_person=self.wait_person-self.volume #乘客数减去通行量
        self.wait_person=max(0,self.wait_person) #最少为0


    def get_state(self):
        #print(f'{self.id} | wait person {self.wait_person} | origin position {self.origin_position} | destination position {self.destination_position}')
        return(self.origin_position, 
               self.destination_position, 
               self.wait_person) #返回 起点 终点和现在等待的人数