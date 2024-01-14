'''
Author: pangay 1623253042@qq.com
Date: 2024-01-14 21:19:12
LastEditors: pangay 1623253042@qq.com
LastEditTime: 2024-01-14 22:37:55
'''
import sys
from pathlib import Path

parent_directory = Path(__file__).resolve().parent.parent
if str(parent_directory) not in sys.path:
    sys.path.insert(0, str(parent_directory))
    
import numpy as np
from loguru import logger
from tshub.utils.get_abs_path import get_abs_path
from gym import logger, spaces
from stable_baselines3.common.env_checker import check_env

from make_env import make_env


if __name__ == '__main__':

    at_env_generate = make_env(time=100)
    tsc_env = at_env_generate()

    # Check Env
    print(tsc_env.observation_space.sample())
    #print(tsc_env.action_space.n)
    check_env(tsc_env)
    # Simulation with environment
    dones = False
    states, info = tsc_env.reset()
    while not dones:
        action = {}
        action = [0,0,0,0]
        states, rewards, truncated, action, infos = tsc_env.step(action=action)
        #logger.info(f"SIM: {infos['step_time']} \n+State:{states}; \n+Reward:{rewards}.")
    tsc_env.close()
