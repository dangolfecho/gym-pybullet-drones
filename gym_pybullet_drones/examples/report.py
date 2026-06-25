'''
Creates a report

python report.py --from_file True --file_path <schedule_path> --path results/

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

def report(from_file=DEFAULT_FLAG, file_path=DEFAULT_FILE, path=DEFAULT_PATH):
    HEAD_ROW = ['X', 'Y', 'Z', 'R', 'P', 'Y', 'Training epochs', 'Score', 'Max\
    possible', 'Percentage', 'Difference']
    if(not(from_file)):
        list_dirs = os.listdir(path)
        total_write_list = [HEAD_ROW]
        for i in list_dirs:
            interim_list = get_config(i)
            dir_name = path+'/'+i
            with open((dir_name+'/epochs.txt'), 'r') as fp1:
                raw_read = (fp1.readlines())[0]
                num_epochs = float(raw_read.rstrip())
                interim_list.append(num_epochs)
            arr = np.load((dir_name+'/evaluations.npz'))
            score = (np.mean(arr['results'][-1])).item()
            max_score = 474
            interim_list.append(score)#Score
            interim_list.append(max_score)#Max from scaffolded_learning.py
            interim_list.append(float(score/max_score))
            interim_list.append(max_score - score)

            total_write_list.append(interim_list)
        with open("report.csv", 'w', newline='') as fp:
            writer = csv.writer(fp)
            writer.writerows(total_write_list)
    else:
        total_write_list = [HEAD_ROW]
        config_list, full_paths = get_strs(file_path, path)
        for i in range(len(full_paths)):
            interim_list = config_list[i][:-2]
            dir_name = full_paths[i]
            with open((dir_name+'/epochs.txt'), 'r') as fp:
                raw_read = (fp.readlines())[0]
                num_epochs = float(raw_read.rstrip())
                interim_list.append(num_epochs)
            arr = np.load((dir_name+'/evaluations.npz'))
            score = (np.mean(arr['results'][-1])).item()
            max_score = 474
            interim_list.append(score)
            interim_list.append(max_score)
            interim_list.append(float(score/max_score))
            interim_list.append(max_score-score)

            total_write_list.append(interim_list)
        with open("report.csv", "w", newline='') as fp:
            writer = csv.writer(fp)
            writer.writerows(total_write_list)
                



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create a report")
    parser.add_argument('--from_file', type=bool, default=DEFAULT_FLAG,
                        help='True if report needs to be gen from schedule')
    parser.add_argument('--file_path', type=str, default=DEFAULT_FILE,
                        help='Path where schedule is stored')
    parser.add_argument('--path', type=str, default=DEFAULT_PATH,
                        help='Path where files are present')
    args = parser.parse_args()

    report(**vars(args))
