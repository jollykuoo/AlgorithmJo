import pandas as pd
import csv
import numpy
import scipy.special
import ClientClassification.loadData


class NeuralNetWork:
    def __init__(self, inode, hnode, onode, lrate):

        self.innode = inode

        self.hiddennode = hnode

        self.outnode = onode   # nodes of neural network

        self.learnrate = lrate   # learning rate

        self.wih = numpy.random.rand(hnode, inode) - 0.5

        self.who = numpy.random.rand(onode, hnode) - 0.5    # parameter

        self.activation_function = lambda x: scipy.special.expit(x)   # activated function

        pass

    def train(self, input_list, target_list):
        input = numpy.array(input_list, ndmin=2).T
        target = numpy.array(target_list, ndmin=2).T  # transform matrix

        hidden_input = numpy.dot(self.wih, input)
        hidden_output = self.activation_function(hidden_input)  # the first layer

        final_input = numpy.dot(self.who, hidden_output)
        final_output = self.activation_function(final_input)  # the second layer

        if numpy.argmax(final_output) == numpy.argmax(target):
            score = 1
        else:
            score = 0

        output_error = target - final_output

        hidden_error = numpy.dot(self.who.T, output_error)  # return errors

        self.who += self.learnrate * numpy.dot(output_error * final_output * (1 - final_output),
                                               numpy.transpose(hidden_output))

        self.wih += self.learnrate * numpy.dot(hidden_error * hidden_output * (1 - hidden_output),
                                               numpy.transpose(input))   # GradientDescend

        return score

        pass

    def query(self, input_list, target_list):
        input = numpy.array(input_list, ndmin=2).T
        target = numpy.array(target_list, ndmin=2).T  # transform matrix
        goal = numpy.argmax(target)

        hidden_input = numpy.dot(self.wih, input)
        hidden_output = self.activation_function(hidden_input)  # the first layer in/out

        final_input = numpy.dot(self.who, hidden_output)
        final_output = self.activation_function(final_input)  # the second layer in/out

        if numpy.argmax(final_output) == goal:
            return 1
        else:
            return 0

        pass

    def exam(self, input_list):
        wih = pd.read_csv("~/PycharmProjects/Classification/ClientClassification/wih.csv").values
        who = pd.read_csv("~/PycharmProjects/Classification/ClientClassification/who.csv").values
        # reload parameter

        hidden_input = numpy.dot(wih, input_list)
        hidden_output = self.activation_function(hidden_input)

        final_input = numpy.dot(who, hidden_output)
        final_output = self.activation_function(final_input)
        return numpy.argmax(final_output)
        pass


def recorrect_data(source, semi_destination, destination, num):
    # correct size of data to boost the accuracy
    # recorrect_data("fullpre.csv","correct_fulldata.csv","correct_fullonehot.csv",50000)
    file = open(semi_destination, "w", encoding="gbk", newline="")
    writer = csv.writer(file)
    writer.writerow(['age', 'job', 'marital', 'education', 'default', 'balance', 'housing', 'loan', 'subscribe'])
    data = pd.read_csv(source)
    negative = 0

    for i in range(len(data)):
        row = data.iloc[i]

        if(row[8] == "no") and negative <= num:
            negative += 1
            writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]])
        elif row[8] == "yes":
            writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]])

    file.close()

    # convert balanced-data to onehot
    ClientClassification.loadData.convert2onehot(pd.read_csv(semi_destination), destination)

    pass


def model_running(trainer):
    prefile = pd.read_csv("correct_fullonehot.csv").values.astype(numpy.float32)
    numpy.random.shuffle(prefile)

    sep = int(0.7 * len(prefile))
    epoch = 7

    data_x = prefile[:sep, :33]
    data_y = prefile[:sep, 33:]
    test_x = prefile[sep:, :33]
    test_y = prefile[sep:, 33:]  # divide data into training/result collection and keep a 3 to 7 proportion

    score_epoch = []

    for j in range(epoch):
        subrecoder = []
        for i in range(len(data_x)):
            subrecoder.append(trainer.train(data_x[i], data_y[i]))
        score_epoch.append(subrecoder)
        print("accuracy = %f" % (numpy.asarray(subrecoder).sum()/len(subrecoder)), "size = %d" % len(subrecoder))

    pd.DataFrame(trainer.wih).to_csv("~/PycharmProjects/Classification/ClientClassification/wih.csv", index=False)
    pd.DataFrame(trainer.who).to_csv("~/PycharmProjects/Classification/ClientClassification/who.csv", index=False)
    # save parameter for doc

    score = []  # record for accuracy

    for i in range(len(test_x)):
        score.append(trainer.query(test_x[i], test_y[i]))
        pass

    print("test_size = %d" % len(score), "accuracy = %f" % (numpy.asarray(score).sum() / len(score)))


def string2onehot(age='middle', job='admin.', marital='single', education='tertiary',
                  default='no', balance='good', housing='yes', loan='no'):
    age_index = {
        'young': 0,
        'middle': 1,
        'preold': 2,
        'old': 3
    }
    job_index = {
        'admin.': 4,
        'blue-collar': 5,
        'entrepreneur': 6,
        'housemaid': 7,
        'management': 8,
        'retired': 9,
        'self-employed': 10,
        'services': 11,
        'student': 12,
        'technician': 13,
        'unemployed': 14,
        'unknown': 15,
    }
    marital_index = {
        'divorced': 16,
        'married': 17,
        'single': 18
    }
    education_index = {
        'primary': 19,
        'secondary': 20,
        'tertiary': 21,
        'unknown': 22
    }
    default_index = {
        'no': 23,
        'yes': 24
    }
    balance_index = {
        'bad': 25,
        'good': 26,
        'ok': 27,
        'soso': 28
    }
    housing_index = {
        'no': 29,
        'yes': 30
    }
    loan_index = {
        'no': 31,
        'yes': 32
    }

    inputs = numpy.zeros([1, 33], dtype=int).T

    inputs[age_index[age]] = 1
    inputs[job_index[job]] = 1
    inputs[marital_index[marital]] = 1
    inputs[education_index[education]] = 1
    inputs[default_index[default]] = 1
    inputs[balance_index[balance]] = 1
    inputs[housing_index[housing]] = 1
    inputs[loan_index[loan]] = 1

    # ->>>>>测试字符转换成模型数据
    # print(inputs.T)

    return inputs

    pass


if __name__ == "__main__":
    # # recorrect_data("fullpre.csv","correct_fulldata.csv","correct_fullonehot.csv",25000)
    # trainer = NeuralNetWork(inode=33, hnode=100, onode=2, lrate=0.15)
    # # model_running(trainer)
    #
    # ##->>>>>>>>测试使用字符输入得出客户类型
    # full_data = pd.read_csv("correct_fulldata.csv").values
    # numpy.random.shuffle(full_data)
    # test_data = full_data[:1000,:8]
    # counter = 0
    # for i in range(len(test_data)):
    #     row = test_data[i]
    #     result = trainer.exam(string2onehot(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
    #     if result == 0:
    #         pass #print("次等用户")
    #     else:
    #         #print("优等用户")
    #         counter += 1
    # print(counter,"proportion=%f"%(counter/1000))
    #
    # # ran = numpy.random.normal(0.0,pow(100,-0.5),(33,1))

    pass
