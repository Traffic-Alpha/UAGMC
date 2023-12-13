'''
Author: PangAY
Date: 2023-12-08 21:13:26
LastEditTime: 2023-12-13 21:40:18
LastEditors: pangay 1623253042@qq.com
'''
from typing import List, Tuple

class Vehicle(object):
    """
    Data describing the vehicle, including vehicle ID, origin position, and speed
    """
    def __init__(
            self,id: str ='0', 
            origin_position: List[int] =[0,0],
            speed: int = 2,
            ) -> None: 
        
        self.id = id
        self.origin_position = origin_position # starting point
        self.speed = speed 
        # speed represents the length of the side traveled per minute
        self.passenger = None # passenger ID
        self.state = 'wait' 
        # have two states， “wait”：wait for match； “drive”, success match passenger，

    def update_state(self, person_id):
        self.state = 'drive'
        self.passenger = person_id # 
    
    def get_drive_time(self, 
                       begin: List[int] , 
                       end: List[int], 
                       rate_ratio: float =1, 
        # congestion coefficient true vehicle speed = vehile speed * rate_ratio
                       ):
        travel_time=(
            abs(begin[0]-end[0]) 
            + abs(begin[1]-end[1]))/(
            self.speed*rate_ratio)
        return travel_time
    

    def get_state(self):
        #print(f'{self.id} | origin_position {self.origin_position} | state {self.state}')
        return({self.id:[self.origin_position]})
    
    def create_object(self):
        
        return self