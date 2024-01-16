'''
Author: PangAY
Date: 2023-12-08 21:33:12
LastEditTime: 2024-01-16 20:53:52
LastEditors: pangay 1623253042@qq.com
'''
import random

from loguru import logger
from typing import Dict, Any
from .vehicle import Vehicle
from at_obj.map.map import Map

class VehicleBuilder(object):

    def __init__(self, vehicle_num: int = 10, ) -> None:
        
        self.map = Map()
        self.vehicles:Dict[str,Vehicle] = {}
        #
        self.vehicle_num = vehicle_num 

    
        for veh in range(0,self.vehicle_num):
            vehicle_id = str(veh) 
            vehicle_info = Vehicle(vehicle_id).create_object()
            self.vehicles[vehicle_id] = vehicle_info

    def create_objects(self, vehicle_id: str)->None:
        origin_position = [
                     random.randint(0, 0.3*self.map.map_len),
                     random.randint(0, 0.3*self.map.map_len)]
        vehicle_info = Vehicle(vehicle_id ,
                               origin_position=origin_position 
                        ).create_object() 
        
        self.vehicles[vehicle_id]=vehicle_info
    

    def __delete_vehicle(self, vehicle_id: str) -> None:
        
        """删除指定 id 的vehicle
        Args:
            vehicle_id (str): vehicle_id id
        """
        if vehicle_id in self.vehicles:
            #logger.info(f"SIM: Delete Vehicle with ID {vehicle_id}.")
            del self.vehicles[vehicle_id] # 匹配成功后自动 unsubscribe
        else:
            logger.warning(f"SIM: Vehicle with ID {vehicle_id} does not exist.")
            
    def update_objects_state(self, time: int) -> None:
        
        """更新场景中所有机动车信息, 包含两个部分:
        1. 对于匹配成功的车辆，将其从 self.vehicles 中删除；
        2. 对于新进入环境的机动车，将其添加在 self.vehicles；
        """
        self.time = time
        del_num = 0 # matched vehicles
        # 删除离开环境的车辆
        for vehicle_id in list(self.vehicles.keys()):
            if self.vehicles[vehicle_id].state == 'drive':
                self.__delete_vehicle(vehicle_id)
                del_num += 1

        # add mew vehicles
        for _ in range(0,del_num):  
            vehicle_id = self.vehicle_num
            self.vehicle_num = self.vehicle_num+1
            self.create_objects(str(vehicle_id))
            
    def get_state(self):
        '''
        for vehicle in  self.vehicles:
            print(self.vehicles[vehicle].get_state())
        '''
        return self.vehicles   