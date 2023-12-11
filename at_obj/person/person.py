'''
Author: PangAY
Date: 2023-12-08 20:51:05
LastEditTime: 2023-12-11 20:50:04
LastEditors: pangay 1623253042@qq.com
'''

from typing import Tuple

class PersonInfo(object):
    """
    """
    def __init__(self, 
                 id: str ='0', 
                 time: int =0,
                 origin_position: list[int,int] =[0,0],
                 destination_position: list[int, int] =[0,0]
            )-> None: 
        
        self.id = id
        # match vehicle_id 
        self.vehicle= None 
        self.origin_position = origin_position
        self.destination_position=destination_position
        # time begin passenger wait for match
        self.begin_time = time 
        # passenger， “wait”：wait for match； “drive”, success match taxi
        self.state='wait' 
        self.wait_time = 0 
    
    def update_state(self, vehicle_id: str):
        self.state = 'drive'
        self.vehicle = vehicle_id
    def get_state(self):
        #print(f'{self.id} | origin_position {self.origin_position} | '
        #      f'destination_position {self.destination_position} | state { self.state}')
        return {self.id:[self.origin_position,
                         self.destination_position]}
    def create_object(self, id: str, time: int, ):
        self.id=id
        self.begin_time = time
        return self
