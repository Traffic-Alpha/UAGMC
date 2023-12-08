'''
Description: 
Author: PangAY
Date: 2023-12-08 20:51:05
LastEditTime: 2023-12-08 22:46:39
LastEditors:  
'''

from typing import Dict, Any
from loguru import logger
from typing import List, Tuple
import random

class PersonInfo(object):
    """
    描述行人的数据，包括行人ID，起始点，终点和出发时间
    """
    def __init__(self, id:str ='0', time:int =0) -> None: #初始化
        
        self.id = id
        self.origin_position = [random.randint(0, 30),random.randint(0, 30)] #起始点
        self.destination_position=[random.randint(70, 99),random.randint(70, 99)]#终点 在地图的位置
        self.begin_time = time #行人出发时间
        self.state='wait' #两种状态 wait， 没有匹配， drive, 匹配成功，

    
    def update_state(self, new_state):
        self.state=new_state

    def get_state(self):
        print(f'{self.id} | origin_position {self.origin_position} | '
              f'destination_position {self.destination_position} | state { self.state}')
        
    def create_object(self, id, time, ):
        self.id=id
        self.begin_time = time
        return self
