import tkinter as tk
import tkinter.ttk as ttk
import numpy
import ClientClassification.neuralNet as Neural
# import DatabaseOperation


class UserInterface:
    def __init__(self, master):
        self.root = master
        self.root.config()
        self.root.title("分类算法")
        self.root.geometry('720x480+200+100')

        SubInterface1(self.root)


class SubInterface1:
    # 决策树分类算法内容页
    def __init__(self, master):
        self.master = master
        self.master.config()

        # 整体框架
        self.frame = tk.Frame(self.master, )

        # 左侧控制栏
        self.frame_left = tk.Frame(self.frame, width=240, height=480, background='white')
        self.frame_left.pack(side='left', fill='y', )

        firstbt = tk.Button(self.frame_left, text="ID-3 决策树算法", command=self.face1)
        firstbt.place(x=60, y=60, width=120, height=50)

        secondbt = tk.Button(self.frame_left, text="贝叶斯算法", command=self.face2)
        secondbt.place(x=60, y=210, width=120, height=50)

        thirdbt = tk.Button(self.frame_left, text="逻辑回归算法", command=self.face3)
        thirdbt.place(x=60, y=360, width=120, height=50)

        # 右侧内容栏
        self.frame_right = tk.Frame(self.frame, width=480, height=480, background='white')

        self.frame_right.pack(side='right', fill='y')

        # pack显示
        self.frame.pack()

    def face1(self):
        pass

    def face2(self):
        self.frame.destroy()
        SubInterface2(self.master)
        pass

    def face3(self):
        self.frame.destroy()
        SubInterface3(self.master)
        pass


class SubInterface2:
    # 贝叶斯分类算法页
    def __init__(self, master):
        self.master = master
        self.master.config()

        # 整体框架
        self.frame = tk.Frame(self.master, )

        # 左侧控制栏
        self.frame_left = tk.Frame(self.frame, width=240, height=480, background='white')
        self.frame_left.pack(side='left', fill='y', )

        firstbt = tk.Button(self.frame_left, text="ID-3 决策树算法", command=self.face1)
        firstbt.place(x=60, y=60, width=120, height=50)

        secondbt = tk.Button(self.frame_left, text="贝叶斯算法", command=self.face2)
        secondbt.place(x=60, y=210, width=120, height=50)

        thirdbt = tk.Button(self.frame_left, text="逻辑回归算法", command=self.face3)
        thirdbt.place(x=60, y=360, width=120, height=50)

        # 右侧内容栏
        self.frame_right = tk.Frame(self.frame, width=480, height=480, background='pink')

        self.frame_right.pack(side='right', fill='y')

        # pack显示
        self.frame.pack()

    def face1(self):
        self.frame.destroy()
        SubInterface1(self.master)
        pass

    def face2(self):
        pass

    def face3(self):
        self.frame.destroy()
        SubInterface3(self.master)
        pass


class SubInterface3:
    # 逻辑回归分类算法页
    def __init__(self, master):
        self.master = master
        self.master.config()

        # 整体框架
        self.frame = tk.Frame(self.master, )

        # 左侧控制栏
        self.frame_left = tk.Frame(self.frame, width=240, height=480, background='white')
        self.frame_left.pack(side='left', fill='y', )

        firstbt = tk.Button(self.frame_left, text="ID-3 决策树算法", command=self.face1)
        firstbt.place(x=60, y=60, width=120, height=50)

        secondbt = tk.ttk.Button(self.frame_left, text="贝叶斯算法", command=self.face2)
        secondbt.place(x=60, y=210, width=120, height=50)

        thirdbt = tk.Button(self.frame_left, text="逻辑回归算法", command=self.face3)
        thirdbt.place(x=60, y=360, width=120, height=50)

        # 右侧内容栏
        self.frame_right = tk.Frame(self.frame, width=480, height=480)

        self.age = tk.Entry(self.frame_right, show=None)  # 年龄输入框
        self.age.pack()

        job_list = ['管理员', '工人', '企业家', '家政', '经理', '退休', '个体户', '服务行业', '学生', '技工', '无业', '未知']
        self.job = ttk.Combobox(self.frame_right, textvariable=tk.StringVar(), values=job_list)  # 职业选择
        self.job.pack()

        marital_list = ['离异', '已婚', '单身']
        self.marital = ttk.Combobox(self.frame_right, textvariable=tk.StringVar(), values=marital_list)  # 婚姻状况
        self.marital.pack()

        education_list = ['小学', '初中', '大学及以上', '未知']
        self.education = ttk.Combobox(self.frame_right, textvariable=tk.StringVar(), values=education_list)  # 学历
        self.education.pack()

        default_list = ['无', '有']
        self.default = ttk.Combobox(self.frame_right, textvariable=tk.StringVar(), values=default_list)  # 有无违约
        self.default.pack()

        self.balance = tk.Entry(self.frame_right, show=None)  # 存款输入
        self.balance.pack()

        housing_list = ['无', '有']
        self.housing = ttk.Combobox(self.frame_right, textvariable=tk.StringVar(), values=housing_list)  # 有无住房
        self.housing.pack()

        loan_list = ['无', '有']
        self.loan = ttk.Combobox(self.frame_right, textvariable=tk.StringVar(), values=loan_list)  # 有无贷款
        self.loan.pack()

        submit = tk.Button(self.frame_right, text='预测')  # 提交
        submit.bind('<ButtonPress-1>', self.process_submit)
        submit.focus_set()
        submit.place(x=10, y=300, width=180, height=25)

        self.esult_label = tk.Label(self.frame_right, text='', fg='blue', font=("黑体", 80))

        self.frame_right.pack(side='right', fill='y')

        # pack显示
        self.frame.pack()

    def face1(self):
        self.frame.destroy()
        SubInterface1(self.master)
        pass

    def face2(self):
        self.frame.destroy()
        SubInterface2(self.master)
        pass

    def face3(self):
        pass

    def process_submit(self, event):
        input = self.string2onthot(float(self.age.get()), self.job.current(), self.marital.current(),
                                   self.education.current(), self.default.current(), float(self.balance.get()),
                                   self.housing.current(), self.loan.current())
        runner = Neural.NeuralNetWork(inode=33, hnode=100, onode=2, lrate=0.15)
        result = runner.exam(input)
        if result == 1:
            print("贷款客户")
        elif result == 0:
            print("非贷款客户")
        pass

    def string2onthot(self,age=30, job_combo=4, marital_combo=18, education_combo=20,
                      default_combo=23, balance=0, housing_combo=30, loan_combo=31):
        # 除年龄和存款之外，其余均为复选框的返回序号

        inputs = numpy.zeros([1, 33], dtype=int).T  # 创造全为0的输入矩阵

        if age < 30:
            age_index = 0
        elif age < 45:
            age_index = 1
        elif age < 60:
            age_index = 2
        else:
            age_index = 3

        if balance < 0:
            balance_index = 25  # bad
        elif balance < 5000:
            balance_index = 28  # soso
        elif balance < 20000:
            balance_index = 27  # ok
        else:
            balance_index = 26  # good

        inputs[age_index] = 1
        inputs[job_combo+4] = 1
        inputs[marital_combo+16] = 1
        inputs[education_combo+19] = 1
        inputs[default_combo+23] = 1
        inputs[balance_index] = 1
        inputs[housing_combo+29] = 1
        inputs[loan_combo+31] = 1

        return inputs


if __name__ == "__main__":
    root = tk.Tk()  # 创建一个空页面
    UserInterface(root)
    root.mainloop()  # loop
