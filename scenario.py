'''
Author: PangAY
Date: 2023-12-08 17:01:38
LastEditTime: 2023-12-13 21:40:38
LastEditors: pangay 1623253042@qq.com
'''
from at_obj.person.person_builder import PersonBuilder
from at_obj.vehicle.vehicle_builder import VehicleBuilder
from at_obj.uam.uam import UAM_Lane

class Scenario(object):
    def __init__(self) -> None:
        
        self.time = 0 # simulate time
        self.persons = PersonBuilder(person_num = 4) # passenger list
        self.vehicles = VehicleBuilder() # vehicles builder 

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
        self.time+=1
        # get passenger list
        person_list=[id for id  in self.persons.person] 
        vehicle_list=[id for id in self.vehicles.vehicles]
        reward={}
        # Time consuming for matching passengers and vehicles
        reward_match_time = 0 
        #
        reward_uam_time = 0
        reward_drive_time = 0
        # Update states and calculate reward
        for person in person_list:
            # match
            self.vehicles.vehicles[vehicle_list[action[person][0]]].update_state(person) 
            self.persons.person[person].update_state(
                vehicle_list[action[person][0]]) 
            # The time it takes for a matching taxi to pick up passenger
            reward_match_time = reward_match_time + self.vehicles.vehicles[
                vehicle_list[action[person][0]]].get_drive_time(
                self.vehicles.vehicles[vehicle_list[action[person][0]]].origin_position,
                self.persons.person[person].origin_position) 
            # passenger choose UAM or ground
            if action[person][1] == 'UAM':
                self.uam.add_new_passenger(self.persons.person[person])
                # Queuing time
                wait_time = self.uam.get_wait_time()
                # Flying time
                fly_time = self.uam.get_fly_time()
                reward_uam_time = reward_uam_time + wait_time + fly_time
                reward_drive_time += self.vehicles.vehicles[
                vehicle_list[action[person][0]]].get_drive_time(
                     self.uam.destination_position,
                     self.persons.person[person].destination_position,
                     ) 
                
            elif action[person][1] == 'ground':
                reward_drive_time += self.vehicles.vehicles[
                vehicle_list[action[person][0]]].get_drive_time(
                     self.persons.person[person].origin_position,
                     self.persons.person[person].destination_position,
                     ) 
    
        reward['reward_match_time'] = reward_match_time
        reward['reward_uam_time'] = reward_uam_time
        reward['reward_drive_time'] = reward_drive_time
        state = {obj_id: self.item[obj_id].get_state() for obj_id in self.item} #get state
        self.uam.update_objects_state(self.time)
        self.vehicles.update_objects_state(self.time)
        self.persons.update_objects_state(self.time)
        
        return state, reward

if __name__ == '__main__':

    # 类的实例化
    car1 = Scenario()
    
    state = car1.reset()

    for _ in range(0,10):
        action = {}
        i = 0
        for people in car1.state['people']:
            #[vehicle_id, if choose UAM] it can chouse 'UAM' or 'ground'
            action[people] = [i,'UAM'] 
            i+=1 
        print('ACTION',action)
        state, reward = car1.step(action)
        print('state',state)
        print('reward',reward)

