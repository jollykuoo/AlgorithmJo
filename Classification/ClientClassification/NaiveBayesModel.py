import pandas as pd
import numpy as np
import sys


class NaiveBayesModel:
    def __init__(self):
        self.smoothing = 1  # 拉普拉斯平滑系数为1

    def calPriorProb(self, data):
        """
        计算各个类的概率
        :param data:训练数据矩阵DataFrame（包含结果，结果的特征名为result）
        :type data:pandas.core.frame.DataFrame
        :return: 先验概率字典   {类：概率}
        """
        self.classCounts = data['result'].value_counts()  # 训练样本中类的数量集合
        self.className = self.classCounts.index.tolist()  # 训练样本中类名称集合
        num = len(data)  # 训练样本总数
        classNum = len(self.classCounts)  # 类的个数
        classPriorProbs = dict()
        for i in range(classNum):
            classPriorProb = (self.classCounts[i] + self.smoothing) / (num + classNum * self.smoothing)
            classPriorProbs.update({self.className[i]: classPriorProb})
        return classPriorProbs

    def discrete(self, trainData, data):
        """
        计算离散数据的条件概率p(特征值|类)
        :param trainData: 训练数据中的离散数据的矩阵DataFrame（包含结果，结果的特征名为result）
        :type trainData:pandas.core.frame.DataFrame
        :param data : 需要预测的离散数据数组list
        :type data:list
        :return :  预测样本的离散值概率字典   {类：{特征(不是特征值)：概率}}}
        """
        # classCounts = trainData['result'].value_counts()  # 训练样本中类的数量集合
        # className = classCounts.index.tolist()  # 训练样本中类名称集合
        featureName = trainData.columns.tolist()[:len(list(trainData.columns)) - 1]  # 获取所有特征名
        discreteProb = dict()  # 存放类别
        for result in self.className:  # 循环类别
            classification = trainData[trainData["result"] == result]  # 按类划分数据集
            feature = {}  # 初始化和重置特征字典
            for i in range(len(data)):  # 循环特征
                values = trainData[featureName[i]].drop_duplicates().tolist()  # 获取某特征的全部特征值
                value = classification[featureName[i]].drop_duplicates().tolist()  # 获取某类别的某特征的全部特征值
                featureCounts = classification[featureName[i]].value_counts()  # 统计训练集第i列元素的值的个数
                if data[i] in value:
                    feature[featureName[i]] = (featureCounts[data[i]] + self.smoothing) / (
                            len(classification) + len(values) * self.smoothing)
                else:  # 如果某特征值在某类中不存在
                    feature[featureName[i]] = self.smoothing / (
                            len(classification) + len(values) * self.smoothing)
            discreteProb.update({result: feature})  # 将概率添加进字典
        return discreteProb

    def continuity(self, trainData, data):
        """
        计算连续数据的概率,用高斯概率密度代替条件概率p(特征值|类)
        :param trainData: 训练数据中的连续数据的矩阵DataFrame（包含结果，结果的特征名为result）
        :type trainData:pandas.core.frame.DataFrame
        :param data : 需要预测的离散数据数组list
        :type data:list
        :return :  预测样本的连续值概率字典   {类：{特征(不是特征值)：概率}}}
        """
        # classCounts = trainData['result'].value_counts()  # 训练样本中类的数量集合
        # className = classCounts.index.tolist()  # 训练样本中类名称集合
        features = trainData.columns.tolist()[:len(list(trainData.columns)) - 1]  # 训练样本中的特征
        meanAndStd = dict()
        for result in self.className:  # 循环类别
            temp = {}
            classification = trainData[trainData["result"] == result]  # 按类别划分数据
            temp['mean'] = classification.mean()  # 类别里各特征均值
            temp['std'] = classification.std()  # 类别里各特征标准差
            meanAndStd[result] = temp

        def calProbabilityDensity(x, mean, std):  # x为待测数据，mean为均值，var为方差,算高斯概率密度
            expTemp = np.exp(- (np.power((x - mean), 2) / (2 * (np.power(std, 2)))))
            if expTemp == 0:  # 数据太小溢出了，暂时不知道咋解决
                expTemp = sys.float_info.min
            pron = 1 / (np.sqrt(2 * np.pi) * std) * expTemp
            return pron

        continuityProbability = dict()
        for result in self.className:
            probability = {}
            for i in range(len(features)):
                probability[features[i]] = calProbabilityDensity(data[i],
                                                                 meanAndStd[result]['mean'][features[i]],
                                                                 meanAndStd[result]['std'][features[i]])
            continuityProbability[result] = probability
        return continuityProbability

    def predict(self, disTrainData, disData, conTrainData, conData):
        """
        预测
        :param disTrainData: 训练数据中的离散数据的矩阵DataFrame（结果的特征名为result）
        :type disTrainData:pandas.core.frame.DataFrame
        :param disData：预测数据中的离散数据列表（和训练数据一一对应）
        :type disData:list
        :param conTrainData：训练数据中的连续数据的矩阵DataFrame（结果的特征名为result）
        :type conTrainData:pandas.core.frame.DataFrame
        :param conData : 预测数据中的连续数据列表list（和训练数据一一对应）
        :type conData:list
        :return :预测结果
        :rtype:str
        """
        # if len(disTrainData) > 0 and len(conTrainData) > 0:  # 同时有离散数据和连续数据
        featureName = disTrainData.columns.tolist()[
                      :len(list(disTrainData.columns)) - 1] + conTrainData.columns.tolist()[
                                                              :len(list(conTrainData.columns)) - 1]
        priorProb = self.calPriorProb(disTrainData)
        probability = self.discrete(disTrainData, disData)
        temp = self.continuity(conTrainData, conData)
        for i in self.className:
            probability[i].update(temp[i])  # 合并两个条件概率字典
        # elif len(disTrainData) > 0:  # 只有离散数据
        #     featureName = disTrainData.columns.tolist()[:len(list(disTrainData.columns)) - 1]
        #     priorProb = self.calPriorProb(disTrainData)
        #     probability = self.discrete(disTrainData, disData)
        # elif len(conTrainData) > 0:  # 只有连续数据
        #     className = conTrainData['result'].value_counts().index.tolist()
        #     featureName = conTrainData.columns.tolist()[:len(list(conTrainData.columns)) - 1]
        #     priorProb = self.calPriorProb(conTrainData)
        #     probability = self.continuity(conTrainData, conData)

        results = dict()
        for i in range(len(probability)):
            pro = 0
            for j in range(len(featureName)):
                pro += np.log(probability[self.className[i]][featureName[j]])  # 各条件概率对数的和（防止数据过小溢出）
            pro += np.log(priorProb[self.className[i]])  # 再和类概率对数相加
            results[self.className[i]] = pro
        result = self.className[0]
        for name in self.className:
            if (results[name] - results[result]) > 0:  # 两对数相减大于零，则被减对数的概率比较大，即为所求结果
                result = name
        return result  # 返回预测结果
