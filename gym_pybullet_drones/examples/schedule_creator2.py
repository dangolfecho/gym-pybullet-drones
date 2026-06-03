"""
schedule looks like
pos_x pos_y pos_z roll pitch yaw training_time load_existing model

if load_existing_model == True, then use old model
other use a new model

position has std units and rpy has radian as units
"""

import argparse

positions = []
roll_pitch_yaws = []
start_pos = []
end_pos = []
start_rpys = []
end_rpys = []
pos_steplength = []

pos_vars = ["x", "y", "z"]
rpy_vars = ["roll", "pitch", "yaw"]

use_prev_model = False
training_time = 1e5

def create():
	for i in range(3):
		x = float(input(f"Enter the starting {pos_vars[i]}\n"))
		y = float(input(f"Enter the ending {pos_vars[i]}\n"))
