''' 
Author: PangAY
Date: 2023-12-08 21:31:06
LastEditTime: 2023-12-13 21:35:54
LastEditors: pangay 1623253042@qq.com
'''
import random

from loguru import logger
from typing import Dict, Any 

from .person import PersonInfo
from at_obj.map.map import Map

class PersonBuilder(object):
    def __init__(self, person_num:int =4, map: Any = Map()) -> None:
        self.map = map
        self.person:Dict[str,PersonInfo] = {}
        self.time=0
        self.person_num=person_num

    def create_objects(self, person_id:str)->None:
        origin_position = [
                     random.randint(0, 0.3*self.map.map_len),
                     random.randint(0, 0.3*self.map.map_len)]
        destination_position=[
                     random.randint(0.7*self.map.map_len, self.map.map_len ),
                     random.randint(0.7*self.map.map_len,self.map.map_len)]
        person_info = PersonInfo(
            person_id, 
            self.time,
            origin_position=origin_position,
            destination_position=destination_position,
        ).create_object(person_id, self.time) 
        
        self.person[person_id]=person_info
        
    def __delete_person(self, person_id: str) -> None:
        
        """删除指定 id 的行人
        Args:
            person_id (str): person_id id
        """
        if person_id in self.person:
            logger.info(f"SIM: Delete Person with ID {person_id}.")
            del self.person[person_id] 
        else:
            logger.warning(f"SIM: Person with ID {person_id} does not exist.")
            
    def update_objects_state(self, time: int) -> None:
        
        """
        Update all passenger information in the scene, including two parts:
        1. For successfully matched pedestrians, delete them from self.people;
        2. For new passenger entering the environment, add them in self.people;
        """
        # Delete successfully matched passengers
        self.time = time
        for person_id in list(self.person.keys()):
            if self.person[person_id].state == 'drive':
                self.__delete_person(person_id)

        #  Updated passenger information
        for num in range(0,self.person_num):  
            person_id =  str(self.time) + '_' + str(num)
            self.create_objects(person_id)
    
    def get_state(self):
        for _ in  self.person:
            print(self.person[_].get_state())
        return self.person
    
    def __call__(self, time: int) -> Any:

        self.time = time