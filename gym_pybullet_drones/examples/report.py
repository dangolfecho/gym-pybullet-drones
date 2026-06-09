'''
Creates a report

python report.py --path results/

Creates report.csv file

'''
import argparse
import csv
import numpy as np
import os


DEFAULT_PATH = '.'


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

def report(path=DEFAULT_PATH):
    HEAD_ROW = ['X', 'Y', 'Z', 'R', 'P', 'Y', 'Training epochs', 'Score', 'Max\
    possible', 'Percentage', 'Difference']
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create a report")
    parser.add_argument('--path', type=str, default=DEFAULT_PATH,
                        help='Path where files are present')
    args = parser.parse_args()

    report(**vars(args))
