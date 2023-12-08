'''
Description: 
Author: PangAY
Date: 2023-12-08 21:31:06
LastEditTime: 2023-12-08 22:46:15
LastEditors:  
'''
from loguru import logger
from typing import Dict, Any
from .person import PersonInfo

class PersonBuilder(object):
    def __init__(self, person_num:int =4) -> None:
        self.people:Dict[str,PersonInfo] = {}
        self.time=0
        self.person_num=person_num

    def create_objects(self, person_id:str)->None:
        
        person_info = PersonInfo(person_id, self.time).create_object(person_id, self.time) #创建一个对象
        
        self.people[person_id]=person_info
        
    #可以假设每次新出现的行人需求都会被满足
    def __delete_person(self, person_id: str) -> None:
        
        """删除指定 id 的行人
        Args:
            person_id (str): person_id id
        """
        if person_id in self.people:
            logger.info(f"SIM: Delete Person with ID {person_id}.")
            del self.people[person_id] # 匹配成功后自动 unsubscribe
        else:
            logger.warning(f"SIM: Person with ID {person_id} does not exist.")
            
    def update_objects_state(self, time) -> None:
        
        """更新场景中所有行人信息, 包含三个部分:
        1. 对于匹配成功的行人，将其从 self.people 中删除；
        2. 对于新进入环境的行人，将其添加在 self.people；
        """
        # 删除离开环境的行人
        self.time = time
        for person_id in list(self.people.keys()):
            if self.people[person_id].state == 'drive': #匹配好的行人的状态是 drive 在此问题中每次新出现的行人都被匹配
                self.__delete_person(person_id)

        # 更新已存在的行人信息
        for _ in range(0,self.person_num):  #每次仿真新增需求点
            person_id =  str(self.time) + '_' + str(_)
            self.create_objects(person_id)
        
    def __call__(self, time) -> Any:

        self.time = time