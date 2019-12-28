from DatabaseOperation import Database
from ClientClassification import NaiveBayesModel
import pandas as pd


class NaiveBayes:
    def output(self):
        database = Database.Database()
        data = database.showAll()
        cus = pd.DataFrame(data,
                           columns=['id', 'name', 'tele', 'age', 'job', 'marital', 'education', 'default', 'balance',
                                    'housing', 'loan',
                                    'result'])
        cus = cus.iloc[:, 3:]
        cus = cus[~cus['job'].isin(['unknown'])]  # 去除job为unkown的数据
        cus = cus[~cus['education'].isin(['unknown'])]  # 去除education为unkown的数据
        cus = cus.apply(pd.to_numeric, errors='ignore')  # 将年龄和余额转为float格式

        def compareAge(age):  # 将年龄转为离散数据
            if age < 18:
                return 0
            for i in range(1, 15):
                if age < (18 + i * 5):
                    return i
            if age > 87:
                return 15

        cus['age'] = cus['age'].apply(lambda x: compareAge(x))
        disTrainData = cus.iloc[:, [0, 1, 2, 3, 4, 6, 7, 8]]
        conTrainData = cus.iloc[:, [5, 8]]
        age0 = float(input("input:age"))  # 输入
        if age0 < 18:
            print('no')
        age = compareAge(age0)
        job = input("input:job")
        marital = input("input:marital")
        education = input("input:education")
        default = input("input:default")
        balance = float(input("input:balance"))
        if balance > 130000:
            balance = 130000
        if balance < -130000:
            balance = -130000
        housing = input("input:housing")
        loan = input("input:loan")  # 输入
        disData = [age, job, marital, education, default, housing, loan]
        conData = [balance]
        # disData = ['18', 'unemployed', 'married', 'primary', 'no', 'no', 'no']
        # conData = [-130000]
        result = NaiveBayesModel.NaiveBayesModel().predict(disTrainData, disData, conTrainData, conData)
        return result


a = NaiveBayes()
print(a.output())  # 预测结果
