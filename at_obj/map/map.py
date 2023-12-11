'''
Author: PangAY
Date: 2023-12-08 22:45:18
LastEditTime: 2023-12-11 20:56:07
LastEditors: pangay 1623253042@qq.com
'''
import numpy as np
class Map(object):
    
    def __init__(self, 
                 origin_position: list[int, int] = [30,30],
                 destination_position: list[int, int] = [70, 70],
                 map_information: list[int, int] = [100,100]
                 ) -> None:
        #  place the plane takes off
        self.vertiport_origin_position = origin_position 
        #  place the plane landed
        self.vertiport_destination_position = destination_position 
        # map information
        self.map_infomation = map_information
        
        self.map_len =  100