'''
Author: pangay 1623253042@qq.com
Date: 2025-05-13 14:55:52
LastEditors: pangay 1623253042@qq.com
LastEditTime: 2025-05-13 14:56:55
FilePath: /UAGMC/test_rl.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
#%%
import torch
from loguru import logger
from tshub.utils.get_abs_path import get_abs_path
from tshub.utils.init_log import set_logger
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecNormalize, SubprocVecEnv

from utilss.sb3_utils import VecNormalizeCallback, linear_schedule
from utilss.make_env import make_env

path_convert = get_abs_path(__file__)
logger.remove()
set_logger(path_convert('./'), file_log_level="INFO", terminal_log_level="INFO")

if __name__ == '__main__':
    # #########
    # Init Env
    # #########
    log_path = path_convert('./log_test/')
    params = {
        'log_file':log_path,
    }
    env =SubprocVecEnv([make_env(env_index=f'{i}', **params) for i in range(1)])
    env = VecNormalize.load(load_path=path_convert('./model_encode_state_5/last_vec_normalize.pkl'), venv=env)
    env.training = False # 测试的时候不要更新
    env.norm_reward = False

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model_path = path_convert('./model_encode_state_5/last_rl_model.zip')
    model = PPO.load(model_path, env=env, device=device)

    # 使用模型进行测试
    obs = env.reset()
    dones = False # 默认是 False
    total_reward = 0

    while not dones:
        action, _state = model.predict(obs, deterministic=True)
        obs, rewards, dones, infos = env.step(action)
        
    env.close()
    print(f'平均等待时间为, {rewards}.')