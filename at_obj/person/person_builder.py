''' 
Author: PangAY
Date: 2023-12-08 21:31:06
LastEditTime: 2024-01-22 13:15:24
LastEditors: pangay 1623253042@qq.com
'''
import random

from loguru import logger
from typing import Dict, Any 

from at_obj.person.person import PersonInfo
from at_obj.map.map import Map

class PersonBuilder(object):
    def __init__(self, person_num:int =4, map: Any = Map()) -> None:
        self.map = map
        self.person:Dict[str,PersonInfo] = {}
        self.person_new: Dict[str,PersonInfo] = {}
        self.time = 0
        self.person_num = person_num
        for num in range(0, person_num): #构建新的人
            person_id =  str(self.time) + '_' + str(num)
            self.create_objects(person_id)
        
    def create_objects(self, person_id:str)->None:
        
        origin_position = [
                     random.randint(0, 0.2*self.map.map_len),
                     random.randint(0, 0.2*self.map.map_len)]
        destination_position=[
                     random.randint(0.8*self.map.map_len, self.map.map_len ),
                     random.randint(0.8*self.map.map_len,self.map.map_len)]
        person_info = PersonInfo(
            person_id, 
            self.time,
            origin_position=origin_position,
            destination_position=destination_position,
        ).create_object(person_id, self.time) 
        
        self.person_new[person_id]=person_info
       
        
    def __delete_person(self, person_id: str) -> None:
        
        """删除指定 id 的行人
        Args:
            person_id (str): person_id id
        """
        if person_id in self.person_new: 
            #logger.info(f"SIM: Delete Person with ID {person_id}.")
            del self.person_new[person_id] 
        else:
            logger.warning(f"SIM: Person with ID {person_id} does not exist.")
            
    def update_objects_state(self, time: int) -> None: #重新写 更新要对行人的状态进行更新， 到达目的地的才删除
        
        """
        Update all passenger information in the scene, including two parts:
        1. For successfully matched pedestrians, delete them from self.people;
        2. For new passenger entering the environment, add them in self.people;
        """
        # Delete successfully matched passengers
        self.time = time  #补充行人的状态更新
                #  Updated passenger information
        for person_id in list(self.person_new.keys()):
            if self.person_new[person_id].state == 'v':
                self.person[person_id] = self.person_new[person_id]
                self.__delete_person(person_id)

        for person_id in list(self.person.keys()):  # 先进行状态更新 再进行删除
            if self.person[person_id].state != 'del': # 如何到达终点 
               self.person[person_id].update_state()
                #self.__delete_person(person_id)

        for num in range(0,self.person_num):  #进入新的行人
            person_id =  str(self.time) + '_' + str(num)
            self.create_objects(person_id)
    def get_all_person(self):
        
        return self.person
    
    def get_state(self):

        return self.person_new
    
    def __call__(self, time: int) -> Any:

        self.time = time
    