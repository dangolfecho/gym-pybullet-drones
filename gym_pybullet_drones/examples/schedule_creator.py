"""
schedule looks like
pos_x pos_y pos_z roll pitch yaw training_time load_existing_model

if load existing model == True, then use old model
otherwise new run

std coords and radians

"""
import argparse

positions = []
roll_pitch_yaws = []

start_pos = []
end_pos = []
start_rpys = []
end_rpys = []
pos_steplength = []
rpy_steplength = []

pos_vars = ["x", "y", "z"]
rpy_vars = ["roll", "pitch", "yaw"]

use_prev_model = False
training_time = 1e5

def create():
	for i in range(3):
		x = float(input(f"Enter the starting {pos_vars[i]}\n"))
		y = float(input(f"Enter the ending {pos_vars[i]}\n"))
		z = float(input("Enter the step size\n"))
		start_pos.append(x)
		end_pos.append(y)
		pos_steplength.append(z)
	for i in range(3):
		x = float(input(f"Enter the starting {rpy_vars[i]}\n"))
		y = float(input(f"Enter the ending {rpy_vars[i]}\n"))
		z = float(input("Enter the step size\n"))
		start_rpys.append(x)
		end_rpys.append(y)
		rpy_steplength.append(z)
	x = input("Do you want to use previously existing models or do you want to train a model from scratch\n Enter y for yes if you want to use existing models and n for no if you want to train a model from scratch")
	if(x == 'n' or x == 'N'):
		use_prev_model = True
	x = int(input("Enter the exponent of the number of 10 ** x training steps required\n"))
	training_time = 10**(x)

	i = start_pos[0]
	with open("schedule.txt", "w") as fp:
		while(i <= end_pos[0]):
			j = start_pos[1]
			while(j <= end_pos[0]):
				k = start_pos[2]
				while(k <= end_pos[2]):
					a = start_rpys[0]
					while(a <= end_rpys[0]):
						b = start_rpys[1]
						while(b <= end_rpys[1]):
							c = start_rpys[2]
							while(c <= end_rpys[2]):
								fp.write(f"{i} {j} {k} {a} {b} {c} {training_time} {int(use_prev_model)}\n")
								c += rpy_steplength[2]
							b += rpy_steplength[1]
						a += rpy_steplength[0]
					k += pos_steplength[2]
				j += pos_steplength[1]
			i += pos_steplength[0]
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Schedule creator')
	parser.add_argument('--default',         default=DEFAULT_MA,            type=str2bool,      help='False goes to input mode, True uses preset', metavar='')
 	ARGS = parser.parse_args()
	print(ARGS)
