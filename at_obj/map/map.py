'''
Description: 
Author: PangAY
Date: 2023-12-08 22:45:18
LastEditTime: 2023-12-08 23:13:08
LastEditors:  
'''
from loguru import logger
from typing import List, Tuple
import random

class Map(object):
    
    def __init__(self) -> None:
        
        self.vertiport_origin_position = [30,30]
        self.vertiport_destination_position = [70,70]