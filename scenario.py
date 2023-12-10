'''
Description: 
Author: PangAY
Date: 2023-12-08 17:01:38
LastEditTime: 2023-12-10 21:41:29
LastEditors: pangay 1623253042@qq.com
'''
from at_obj.person.person_builder import PersonBuilder
from at_obj.vehicle.vehicle_builder import VehicleBuilder
from at_obj.uam.uam import UAM_Lane

class Scenario(object):
    def __init__(self) -> None:
        self.time = 0 # 全局时间
        self.persons = PersonBuilder() # people
        self.vehicles = VehicleBuilder() #vehicles\

        self.uam=UAM_Lane()
        self.item = {
            'vehicle': self.vehicles,
            'people':  self.persons,
            'UAM': self.uam,
        }
        self.state = {obj_id: self.item[obj_id].get_state() for obj_id in self.item}
    
    def reset(self):
        self.persons.update_objects_state(self.time)
        self.vehicles.update_objects_state(self.time)
        state = {obj_id: self.item[obj_id].get_state() for obj_id in self.item}
        return state
    def step(self, action):
        # 调用 step 之后，会 update 所有 person, vehicles 的状态
        # info = {obj_id: obj.get_state() for obj_id, obj in self.x}
        # 更新乘客列表，一次一次来，状态变量有所有行人的位置和所有车的位置，列向量
        self.time+=1
        person_list=[id for id  in self.persons.person] #获取乘客列表
        vehicle_list=[id for id in self.vehicles.vehicles]
        state = {obj_id: self.item[obj_id].get_state() for obj_id in self.item}
        for person in person_list:
            self.vehicles.vehicles[vehicle_list[action[person]]].update_state(person) #匹配
            self.persons.person[person].update_state(vehicle_list[action[person]]) #
        self.vehicles.update_objects_state(self.time)
        self.persons.update_objects_state(self.time)
        
        return state

if __name__ == '__main__':

    # 类的实例化
    car1 = Scenario()
    
    state = car1.reset()

    for _ in range(0,10):
        action = {}
        i = 0
        for _ in car1.state['people']:
            action[_] = i
            i+=1 
        print('ACTION',action)
        state = car1.step(action)
        print('state',state)

