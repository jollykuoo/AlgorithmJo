import pandas as pd
import csv


def load_primarydata():
    # use pandas to load the data structure
    data = pd.read_csv("bank-full.csv", sep=";").drop(["contact", "day", "month", "duration",
                                                      "campaign", "pdays", "previous", "poutcome"], axis=1)
    return data
    pass


def data2file(data):
    # create a csv file to store the useful data from the intergate data
    file = open("fullpre.csv", "w", encoding="gbk", newline="")
    writer = csv.writer(file)
    writer.writerow(['age', 'job', 'marital', 'education', 'default', 'balance', 'housing', 'loan', 'subscribe'])
    for i in range(len(data)):
        row = list(data.iloc[i])   # ix and iloc have the same ability

        # divide age into 4 class
        if row[0] < 30:
            row[0] = 'young'
        elif row[0] < 45:
            row[0] = 'middle'
        elif row[0] < 60:
            row[0] = 'preold'
        else:
            row[0] = 'old'

        # divide balance into 4 class
        if row[5] < 0:
            row[5] = 'bad'
        elif row[5] < 5000:
            row[5] = 'soso'
        elif row[5] < 20000:
            row[5] = 'ok'
        else:
            row[5] = 'good'

        writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]])
    file.close()


def convert2onehot(data, name):
    # covert data to onehot
    onehot = pd.get_dummies(data, prefix=data.columns)
    onehot.to_csv(name, index=False, )

    # return pd.get_dummies(data, prefix=data.columns)
