'''
Description: 
Author: PangAY
Date: 2023-12-08 21:33:12
LastEditTime: 2023-12-08 22:47:12
LastEditors:  
'''

from loguru import logger
from typing import Dict, Any
from .vehicle import Vehicle


class VehicleBuilder(object):


    def __init__(self, vehicle_num:int = 10) -> None:
        
        self.vehicles:Dict[str,Vehicle] = {}
        self.vehicle_num = vehicle_num
    
        for _ in range(0,self.vehicle_num): #初始化出租车对列
            vehicle_id = str(_) 
            vehicle_info = Vehicle(vehicle_id).create_object()
            self.vehicles[vehicle_id] = vehicle_info

    def create_objects(self, vehicle_id:str)->None:
        
        vehicle_info = Vehicle(vehicle_id).create_object() #创建一个对象
        self.vehicles[vehicle_id]=vehicle_info
    #可以假设每次新出现的行人需求都会被满足

    def __delete_vehicle(self, vehicle_id: str) -> None:
        
        """删除指定 id 的vehicle
        Args:
            vehicle_id (str): vehicle_id id
        """
        if vehicle_id in self.vehicles:
            logger.info(f"SIM: Delete Person with ID {vehicle_id}.")
            del self.vehicles[vehicle_id] # 匹配成功后自动 unsubscribe
        else:
            logger.warning(f"SIM: Person with ID {vehicle_id} does not exist.")
            
    def update_objects_state(self, time) -> None:
        
        """更新场景中所有机动车信息, 包含三个部分:
        1. 对于匹配成功的行人，将其从 self.people 中删除；
        2. 对于新进入环境的机动车，将其添加在 self.people；
        """
        self.time = time
        del_num = 0 #删除车辆数量
        # 删除离开环境的行人
        for vehicle_id in list(self.vehicles.keys()):
            if self.vehicles[vehicle_id].state == 'drive':
                self.__delete_vehicle(vehicle_id)
                del_num += 1

        # 补充车辆
        for _ in range(0,del_num):  #每次仿真新增需求点
            vehicle_id = self.vehicle_num+1
            self.create_objects(str(vehicle_id))