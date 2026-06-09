"""Script demonstrating the use of `gym_pybullet_drones`'s Gymnasium interface.

Classes HoverAviary and MultiHoverAviary are used as learning envs for the PPO algorithm.

Modified to allow changes to initial position and orientation as well as ways to automate the iteration process.
Derived from learn.py

Example
-------
In a terminal, run as:

    $ python scaffolded_learning.py 
    $ python scaffolded_learning.py

Notes
-----
This is a minimal working example integrating `gym-pybullet-drones` with 
reinforcement learning library `stable-baselines3`.

3. only single agent for now.

"""
import os
import time
from datetime import datetime
import argparse
import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import torch
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold
from stable_baselines3.common.evaluation import evaluate_policy

from gym_pybullet_drones.utils.Logger import Logger
from gym_pybullet_drones.envs.HoverAviary import HoverAviary
from gym_pybullet_drones.envs.MultiHoverAviary import MultiHoverAviary
from gym_pybullet_drones.utils.utils import sync, str2bool
from gym_pybullet_drones.utils.enums import ObservationType, ActionType

DEFAULT_GUI = True
DEFAULT_RECORD_VIDEO = False
DEFAULT_OUTPUT_FOLDER = 'results'
DEFAULT_COLAB = False
DEFAULT_SC = 'schedule.txt'

DEFAULT_OBS = ObservationType('kin') # 'kin' or 'rgb'
DEFAULT_ACT = ActionType('one_d_rpm') # 'rpm' or 'pid' or 'vel' or 'one_d_rpm' or 'one_d_pid'
DEFAULT_AGENTS = 2
DEFAULT_MA = False

start_pos = np.array([[0, 0, 0.5]])
start_rpy = np.array([[0, 1.57, 1.57]])

def read_schedule(path):
    sch_list = []
    with open(path, "r") as fp:
        for line in fp:
            parts = line.split()
            for i in range(8):
                parts[i] = float(parts[i])
            sch_list.append(parts)
    return sch_list

def give_str(num):
    if num < 0:
        return 'm'+str(-num)
    return str(num)


def modified_run(schedule_path=DEFAULT_SC, multiagent=DEFAULT_MA, output_folder=DEFAULT_OUTPUT_FOLDER, gui=DEFAULT_GUI, plot=True, colab=DEFAULT_COLAB, record_video=DEFAULT_RECORD_VIDEO, local=True):
    schedule = read_schedule(schedule_path)
    for config in schedule:
        start_pos = np.array([[config[0], config[1], config[2]]])
        start_rpy = np.array([[config[3], config[4], config[5]]])
        training_time = config[6]
        use_prev_model = bool(config[7])

        filename = os.path.join(output_folder,
                                'save-'+'x'+give_str(config[0])+'y'+give_str(config[1])+'z'+give_str(config[2])+'r'+give_str(config[3])+'p'+give_str(config[4])+'y'+give_str(config[5]))

        train_env = make_vec_env(HoverAviary,
                                 env_kwargs=dict(obs=DEFAULT_OBS,
                                                 act=DEFAULT_ACT,
                                                 initial_xyzs=start_pos,
                                                 initial_rpys=start_rpy),
                                 n_envs=1,
                                 seed=0)
        eval_env = HoverAviary(obs=DEFAULT_OBS, act=DEFAULT_ACT,
                               initial_xyzs=start_pos,
                               initial_rpys=start_rpy)
        
        print('[INFO] Action space:', train_env.action_space)
        print('[INFO] Observation space:', train_env.observation_space)

        if not os.path.exists(filename):
            os.makedirs(filename+'/')
            model = PPO('MlpPolicy',
                        train_env,
                        # tensorboard_log=filename + '/tb'/',
                        verbose=1)

        else:
            if use_prev_model:
                model = PPO.load(filename+'/best_model.zip',
                                 train_env,
                                 verbose=1)
            else:
                model = PPO('MlpPolicy',
                            train_env,
                            # tensorboard_log=filename + '/tb'/',
                            verbose=1)


        if DEFAULT_ACT == ActionType.ONE_D_RPM:
            target_reward = 474

        else:
            target_reward = 467

        callback_on_best = StopTrainingOnRewardThreshold(reward_threshold=target_reward,
                                      verbose=1)

        eval_callback = EvalCallback(eval_env,
                                     callback_on_new_best=callback_on_best,
                                     verbose=1,
                                     best_model_save_path=filename+'/',
                                     log_path=filename+'/',
                                     eval_freq=int(1000),
                                     deterministic=True,
                                     render=False)
        model.learn(total_timesteps=training_time if local else int(1e2),
                    callback=eval_callback,
                    log_interval=100)

        # Saving the model
        textfile_name = os.path.join(filename+'/epochs.txt')
        if(os.path.isfile(textfile_name)):
            raw_read = ''
            with open(textfile_name, 'r') as fp:
                raw_read = (fp.readlines())[0]
            exis_count = float(raw_read.rstrip())
            exis_count += training_time
            with open(textfile_name, 'w') as fp:
                fp.write(str(exis_count)+'\n')
        else:
            with open(textfile_name, 'w') as fp:
                fp.write(str(training_time)+'\n')

        model.save(filename+'/final_model.zip')

if __name__ == '__main__':
    #### Define and parse (optional) arguments for the script ##
    parser = argparse.ArgumentParser(description='Single agent reinforcement learning example script')
    parser.add_argument('--schedule_path', default=DEFAULT_SC, type=str, help='Which\
    schedule file to use')
    parser.add_argument('--multiagent',         default=DEFAULT_MA,            type=str2bool,      help='Whether to use example LeaderFollower instead of Hover (default: False)', metavar='')
    parser.add_argument('--gui',                default=DEFAULT_GUI,           type=str2bool,      help='Whether to use PyBullet GUI (default: True)', metavar='')
    parser.add_argument('--record_video',       default=DEFAULT_RECORD_VIDEO,  type=str2bool,      help='Whether to record a video (default: False)', metavar='')
    parser.add_argument('--output_folder',      default=DEFAULT_OUTPUT_FOLDER, type=str,           help='Folder where to save logs (default: "results")', metavar='')
    parser.add_argument('--colab',              default=DEFAULT_COLAB,         type=bool,          help='Whether example is being run by a notebook (default: "False")', metavar='')
    ARGS = parser.parse_args()
	
	
    modified_run(**vars(ARGS))
