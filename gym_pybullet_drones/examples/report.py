'''
Creates a report

'''
import csv


DEFAULT_PATH = '.'


def get_config(filename):
    raw_config = filename.split('-'))[1]
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
    return arr

def report(path=DEFAULT_PATH):
    HEAD_ROW = ['X', 'Y', 'Z', 'R', 'P', 'Y', 'Training epochs', 'Score', 'Max
    possible', 'Percentage', 'Difference']
    list_dirs = os.listdir(path)

    with open("report.csv", 'w', newline='') as fp:
        writer = csv.writer(fp)
        writer.
        for i in list_dirs:
            config = get_config(i)

            with open(('i'+'/epochs.txt'), 'r') as fp1:
                raw_read = (fp1.readline())[0]
            num_epochs = float(raw_read.rstrip())

            config.append(num_epochs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create a report")
    parser.add_argument('--path', type=str, default=DEFAULT_MODEL_PATH,
                        help='Path where files are present')
    args = parser.parse_args()

    report(**vars(args))
