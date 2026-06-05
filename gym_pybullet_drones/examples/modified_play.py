'''
modified play.py to set up intial positions and roll pitch yaw based on file
name

currently for single agent case

python modified_play.py --model_path <path>/
'''
import os
import time
import argparse
import numpy as np
import gymnasium as gym
from stable_baselines3 import PPO
from gym_pybullet_drones.envs.HoverAviary import HoverAviary
from gym_pybullet_drones.envs.MultiHoverAviary import MultiHoverAviary
from gym_pybullet_drones.utils.enums import ObservationType, ActionType
from gym_pybullet_drones.utils.utils import sync
from gym_pybullet_drones.utils.Logger import Logger

DEFAULT_MODEL_PATH = "results/best_model.zip"
DEFAULT_GUI = True
DEFAULT_OBS = ObservationType('kin')
DEFAULT_ACT = ActionType('one_d_rpm')
DEFAULT_AGENTS = 2
DEFAULT_MA = False

def play(model_path=DEFAULT_MODEL_PATH, multiagent=DEFAULT_MA, gui=DEFAULT_GUI):
    #### Load saved model ####
    if not os.path.isfile(model_path):
        print(f"[ERROR] Model file not found at: {model_path}")
        return
    #assume file name is results/save-<>/best_model.zip
    raw_config = ((model_path.split('/'))[1].split('-'))[1]
    mode = True
    temp = ''
    arr = []
    for j in range(1, len(raw_config)):
        i = raw_config[j]
        if i!='.' and i.isalpha():
            arr.append(float(temp))
            temp = ''
        elif(j == len(raw_config)-1):
            temp += i
            arr.append(float(temp))
            temp = ''
        else:
            temp += i
    start_pos = np.array([arr[:3]])
    start_rpy = np.array([arr[3:]])
                         
    model = PPO.load(model_path)
    print(f"[INFO] Loaded model from {model_path}")

    #### Create test environment ####
    if not multiagent:
        env = HoverAviary(gui=gui, obs=DEFAULT_OBS, act=DEFAULT_ACT,
                          initial_xyzs=start_pos,
                          initial_rpys=start_rpy)
    else:
        env = MultiHoverAviary(gui=gui, num_drones=DEFAULT_AGENTS, obs=DEFAULT_OBS, act=DEFAULT_ACT)

    logger = Logger(logging_freq_hz=int(env.CTRL_FREQ),
                    num_drones=DEFAULT_AGENTS if multiagent else 1,
                    output_folder="logs_playback/",
                    colab=False)

    #### Run the simulation ####
    obs, _ = env.reset(seed=42, options={})
    start = time.time()

    for i in range((env.EPISODE_LEN_SEC+2)*env.CTRL_FREQ):
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)

        obs2 = obs.squeeze()
        act2 = action.squeeze()

        if DEFAULT_OBS == ObservationType.KIN:
            if not multiagent:
                logger.log(drone=0,
                    timestamp=i/env.CTRL_FREQ,
                    state=np.hstack([obs2[0:3],
                                     np.zeros(4),
                                     obs2[3:15],
                                     act2]),
                    control=np.zeros(12))
            else:
                for d in range(DEFAULT_AGENTS):
                    logger.log(drone=d,
                        timestamp=i/env.CTRL_FREQ,
                        state=np.hstack([obs2[d][0:3],
                                         np.zeros(4),
                                         obs2[d][3:15],
                                         act2[d]]),
                        control=np.zeros(12))

        env.render()
        sync(i, start, env.CTRL_TIMESTEP)
        if terminated:
            break

    env.close()
    logger.plot()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a trained PPO policy in PyBullet drones environment.")
    parser.add_argument('--model_path', type=str, default=DEFAULT_MODEL_PATH, help='Path to saved policy zip file')
    parser.add_argument('--multiagent', type=bool, default=DEFAULT_MA, help='Whether to use MultiHoverAviary')
    parser.add_argument('--gui', type=bool, default=DEFAULT_GUI, help='Enable GUI rendering')
    args = parser.parse_args()

    play(**vars(args))
