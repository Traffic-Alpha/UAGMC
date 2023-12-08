'''
Description: 
Author: PangAY
Date: 2023-12-08 17:01:38
LastEditTime: 2023-12-08 22:44:52
LastEditors:  
'''
from at_obj.person.person_builder import PersonBuilder
from at_obj.vehicle.vehicle_builder import VehicleBuilder
from at_obj.uam.uam import UAM_Lane

class Scenario(object):
    def __init__(self) -> None:
        self.time = 0 # 全局时间
        self.persons = PersonBuilder() # people
        self.vehicles = VehicleBuilder()
        self.persons.update_objects_state(self.time)
        self.vehicles.update_objects_state(self.time)
        self.uam=UAM_Lane()
        self.x = {
            'vehicle':self.vehicles,
            'people': self.persons
        }
    
    def step(self):
        # 调用 step 之后，会 update 所有 person, vehicles 的状态
        # info = {obj_id: obj.get_state() for obj_id, obj in self.x}
        # return info
        pass

if __name__ == '__main__':

    # 类的实例化
    car1 = Scenario()
    print(car1.persons.people)
    print(car1.vehicles.vehicles)
