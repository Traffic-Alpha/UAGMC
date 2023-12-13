'''
Author: PangAY
Date: 2023-12-08 22:45:18
LastEditTime: 2023-12-13 21:35:17
LastEditors: pangay 1623253042@qq.com
'''
import numpy as np
from typing import List
class Map(object):
    
    def __init__(self, 
                 origin_position: List[int] = [30,30],
                 destination_position: List[int] = [70, 70],
                 map_size: List[int] = [100,100],
                 map_imformaton: int = [[]*100,[]*100] 
                 ) -> None:
        
        #  place the plane takes off
        self.vertiport_origin_position = origin_position 
        #  place the plane landed
        self.vertiport_destination_position = destination_position 
        # map size
        self.map_len =  map_size[0]
        self.map_information = map_imformaton