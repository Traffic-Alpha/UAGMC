'''
Author: PangAY
Date: 2023-12-08 20:51:05
LastEditTime: 2024-01-20 22:55:27
LastEditors: pangay 1623253042@qq.com
'''
from typing import List

class PersonInfo(object):
    """
    """
    def __init__(self, 
                 id: str = '0', 
                 time: int = 0,
                 origin_position: List[int] =[0,0],
                 destination_position: List[int] =[0,0]
            )-> None: 
        
        self.id = id
        # match vehicle_id 
        self.vehicle_id = None 
        self.vehicle_speed = 0
        self.origin_position = origin_position
        self.destination_position = destination_position
        self.uam_drive_traval = 0 # 乘坐 UAM 到达UAM机场的距离
        self.destination_drive_traval = 0 #从 UAM 机场到目的地的距离
        self.ground_drive_traval = 0 # 乘坐地面交通距离终点的距离
        # time begin passenger wait for match
        self.begin_time = time 
        # passenger， “wait”：wait for match； “drive”, success match taxi
        self.state='n' # state n：new and not match w: wait v：vehicle drive  a：air taxi  d：arrive destination vd：vehicle to destination  del：计算完reward
        self.method = 'none' # ground 地面交通；UAM 乘坐空中交通 none 还没有决策
        self.wait_time = 0
        self.uam_wait_time = 0 # uam排队等待时间
        self.fly_time = 0 #飞行所需要的时间 
        self.travel_time = 0 # 从起点开始行使的时间
    
    def match_vehicle(self, vehicle):
        self.state = 'v'
        self.vehicle_id = vehicle.id
        self.vehicle_speed = vehicle.speed
    
    def update_state(self):
        # 更新行人状态
        #print('person',self.state)
        if self.method == 'ground':
            if self.state == 'v':
                self.ground_drive_traval -= 1
                if self.ground_drive_traval <= 0:
                    self.state = 'd'

        if self.method == 'UAM' :
            if self.state == 'v' :
                self.uam_drive_traval -= 1
                if self.uam_drive_traval <= 0:
                    self.state = 'arrive'
            elif self.state == 'w':
                self.uam_wait_time -= 1
                if  self.uam_wait_time <= 0:
                    self.state = 'a'
            elif self.state == 'a':
                self.fly_time -= 1
                if  self.fly_time <= 0:
                    self.state = 'vd'
            elif self.state == 'vd':
                self.destination_drive_traval -= 1
                if  self.destination_drive_traval <= 0: 
                    self.state = 'd'

    def get_state(self):
        #print(f'{self.id} | origin_position {self.origin_position} | '
        #      f'destination_position {self.destination_position} | state { self.state}')
        return {self.id:[self.origin_position,
                         self.destination_position]}
    
    def create_object(self, id: str, time: int, ):
        self.state = 'o'
        self.id = id
        self.begin_time = time
        return self
