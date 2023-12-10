'''
Description: 
Author: PangAY
Date: 2023-12-08 22:45:18
LastEditTime: 2023-12-10 21:45:28
LastEditors: pangay 1623253042@qq.com
'''
from loguru import logger
from typing import List, Tuple
import random

class Map(object):
    
    def __init__(self) -> None:
        self.map_len = 100
        self.vertiport_origin_position = [30,30] #起飞点的位置
        self.vertiport_destination_position = [70,70] #降落点的位置