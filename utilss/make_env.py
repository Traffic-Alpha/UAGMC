'''
Author: pangay 1623253042@qq.com
Date: 2024-01-11 21:24:41
LastEditors: pangay 1623253042@qq.com
LastEditTime: 2024-01-17 22:12:42
FilePath: /Air_Taxi_simulation/utils/make_env.py
'''
import sys
from pathlib import Path

parent_directory = Path(__file__).resolve().parent
if str(parent_directory) not in sys.path:
    sys.path.insert(0, str(parent_directory))
 
import gymnasium as gym

from gym import logger, spaces
from utilss.at_wrapper import atWrapper
from stable_baselines3.common.monitor import Monitor
from at_obj.scenario import Scenario
def make_env(
        time:int = 100, 
        log_file:str = 'Log.log', env_index:int = 1,
        ):

    
    def _init() -> gym.Env: 
        at_scenario = Scenario()
        at_wrapper = atWrapper(at_scenario)
        
        return Monitor(at_wrapper, filename=f'{log_file}/{env_index}')
    
    return _init


