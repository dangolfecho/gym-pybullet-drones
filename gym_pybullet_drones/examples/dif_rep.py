'''
Writes difference in performance between two training runs
train1_score - train2_score

python dif_rep.py --f1 <file1> --f2 <file2>

Creates report.csv file

'''
import argparse
import csv
import numpy as np
import os


DEFAULT_PATH = '.'
DEFAULT_FILE = 'schedule.txt'
DEFAULT_FLAG = False

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

def get_strs(file_path, dir_path):
    sch_list = read_schedule(file_path)

    arr = []
    base = dir_path
    for config in sch_list:
        filename = os.path.join(dir_path,
                                'save-'+'x'+give_str(config[0])+'y'+give_str(config[1])+'z'+give_str(config[2])+'r'+give_str(config[3])+'p'+give_str(config[4])+'y'+give_str(config[5]))
        arr.append(filename)
    return (sch_list, arr)
            

def get_config(filename):
    raw_config = filename.split('-')[1]
    temp = ''
    arr = []
    m_flag = False
    for j in range(1, len(raw_config)):
        i = raw_config[j]
        if i!='.' and i.isalpha():
            if(i == 'm'):
                m_flag = True
            else:
                if(m_flag):
                    arr.append(-1 * float(temp))
                    temp = ''
                    m_flag = False
                else:
                    arr.append(float(temp))
                    temp = ''
        elif(j == len(raw_config)-1):
            temp += i
            if(m_flag):
                arr.append(-1 * float(temp))
            else:
                arr.append(float(temp))
            temp = ''
        else:
            temp += i
    return arr

def report(schedule='', path1='', path2=''):
    if(schedule == '' or path1 == '' or path2 == ''):
        return
    HEAD_ROW = ['X', 'Y', 'Z', 'R', 'P', 'Y', 'Training epochs', 'Score', 'Max\
    possible', 'Percentage', 'Difference']
    total_write_list = [HEAD_ROW]
    config_list, f1_full_paths = get_strs(schedule, path1)
    _, f2_full_paths = get_strs(schedule, path2)
    for i in range(len(f1_full_paths)):
        interim_list = config_list[i][:-2]
        dir_name = f1_full_paths[i]
        with open((dir_name+'/epochs.txt'), 'r') as fp:
            raw_read = (fp.readlines())[0]
            num_epochs = float(raw_read.rstrip())
            interim_list.append(num_epochs)
        arr = np.load((dir_name+'/evaluations.npz'))
        score = (np.mean(arr['results'][-1])).item()
        interim_list.append(score)

        total_write_list.append(interim_list)
    print(total_write_list)
    for i in range(len(f2_full_paths)):
        dir_name = f2_full_paths[i]
        with open((dir_name+'/epochs.txt'), 'r') as fp:
            raw_read = (fp.readlines())[0]
            num_epochs = float(raw_read.rstrip())
        arr = np.load((dir_name+'/evaluations.npz'))
        score = (np.mean(arr['results'][-1])).item()

        total_write_list[i+1][-1] = (total_write_list[i+1][-1] - score)
    with open("difference.csv", "w", newline='') as fp:
        writer = csv.writer(fp)
        writer.writerows(total_write_list)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Checks difference between two\
                                     reports")
    parser.add_argument('--schedule', type=str, default=DEFAULT_FILE,
                        help='Path where schedule is stored')
    parser.add_argument('--path1', type=str, default=DEFAULT_FILE,
                        help='Path where first run files are stored')
    parser.add_argument('--path2', type=str, default=DEFAULT_FILE,
                        help='Path where second run files are stored')
    args = parser.parse_args()

    report(**vars(args))
