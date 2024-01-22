'''
Author: pangay 1623253042@qq.com
Date: 2024-01-16 20:38:03
LastEditors: pangay 1623253042@qq.com
LastEditTime: 2024-01-21 23:01:25
'''

import sys
from pathlib import Path

import numpy as np
from gym import logger, spaces
from stable_baselines3.common.env_checker import check_env

from utilss.make_env import make_env


def greedy_policy(state):
    action = [0,0,0,0]
    persons_station = state[3:]
    for i in range(0,4):
        person_station = persons_station[i,:]
        drive_time = get_drive_time(person_station)
        uam_time = get_uam_time(state[1])
        if uam_time < drive_time:
            action[i] = 1 
    return action

def get_drive_time(person_station):
    travel_time=(
            abs(person_station[0]-person_station[2]) 
            + abs(person_station[1]-person_station[3])
            )/2 # manhattan distance
    return travel_time

def get_uam_time(state):
    uam_time = state[1] + state[2]
    return uam_time

at_env_generate = make_env(log_file = 'greedy.log')
tsc_env = at_env_generate()
states, _ = tsc_env.reset()
dones = False
rewards = 0
while not dones:
    action = greedy_policy(states)
    states, reward, truncated, dones, infos = tsc_env.step(action=action)
    rewards += reward
tsc_env.close()

print('rewarde',rewards)