import pymysql
import csv


class Database:
    def __init__(self):
        self.config = {'host': '127.0.0.1',
                       'user': 'root',
                       'password': 'root',
                       'port': 3306,
                       'database': 'customers',
                       'charset': 'utf8'}

    def createTable(self):  # 创建customer表，如果表存在，则删除原有的表
        # 连接数据库
        conn = pymysql.connect(**self.config)
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
        cursor.execute("drop table if exists customer")  # 如果表存在，则删除原有的表
        sql = """CREATE TABLE `customer` 
        (`id` int(11) NOT NULL AUTO_INCREMENT ,
        `name` varchar(45) DEFAULT NULL,
        `tele` varchar(45) DEFAULT NULL,
        `age` varchar(45) DEFAULT NULL,
        `job` varchar(45) DEFAULT NULL,
        `marital` varchar(45) DEFAULT NULL,
        `education` varchar(45) DEFAULT NULL,
        `default` varchar(45) DEFAULT NULL,
        `balance` varchar(45) DEFAULT NULL,
        `housing` varchar(45) DEFAULT NULL,
        `loan` varchar(45) DEFAULT NULL,
        `result` varchar(45) NOT NULL,
        PRIMARY KEY (`id`)
        ) ENGINE = InnoDB  DEFAULT CHARSET=utf8MB4"""
        cursor.execute(sql)  # 执行SQL语句
        conn.commit()
        cursor.close()  # 关闭光标对象
        conn.close()  # 关闭数据库连接

    def wrinteInDatabase(self):  # 导入csv文件数据
        f = open('..\\ClientClassification\\bank-full.csv', 'r')
        next(f)  # 不读取列标签
        reader = csv.reader(f)
        customers = []
        for date in reader:
            for customer in date:
                customer = customer.split(';')  # 将；分隔符转换为，分隔符
                customer = [i.strip('"').strip('.') for i in customer]  # 去除数组里多余的'“'和'.'
                cus = customer[:8]
                cus.append(customer[16])
                customers.append(cus)
        # 连接database
        conn = pymysql.connect(**self.config)
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
        # 定义要执行的SQL语句
        sql = """insert into customer (id,age, job,marital,education,`default`,balance,housing,loan,result) values
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        for i in range(len(customers)):
            customers[i].insert(0, i+1)  # 给数组添加id
            # 参数化方式传参
            cursor.execute(sql, customers[i])  # 执行SQL语句
        conn.commit()
        cursor.close()  # 关闭光标对象
        conn.close()  # 关闭数据库连接

    def select(self, name,tele):  # 查询
        # 连接数据库
        conn = pymysql.connect(**self.config)
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
        sql = """select age, job,marital,education,`default`,balance,housing,loan,result from customer where name =  %s and tele   = %s"""
        cursor.execute(sql,(name,tele))
        conn.commit()
        results = cursor.fetchall()  # 结果
        cursor.close()  # 关闭光标对象
        conn.close()  # 关闭数据库连接
        return results  # 返回查询的数据

    def showAll(self):  # 查询全部数据
        # 连接数据库
        conn = pymysql.connect(**self.config)
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
        sql = """select id,name,tele,age, job,marital,education,`default`,balance,housing,loan,result from customer """
        cursor.execute(sql)
        conn.commit()
        results = cursor.fetchall()  # 结果
        cursor.close()  # 关闭光标对象
        conn.close()  # 关闭数据库连接
        return results  # 返回数据

    def update(self, name,tele, data):  # 更新
        # 连接数据库
        conn = pymysql.connect(**self.config)
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
        sql = """UPDATE customer 
        SET  age = %s, 
        job= %s,
        marital=%s,
        education= %s,
        `default`= %s,
        balance= %s,
        housing= %s,
        loan= %s,
        result = %s
        WHERE name = %s and tele =%s"""
        data.insert(9, name)
        data.insert(10, tele)
        cursor.execute(sql, data)  # 执行SQL语句
        conn.commit()
        cursor.close()  # 关闭光标对象
        conn.close()  # 关闭数据库连接

    def delete(self, name,tele):  # 删除
        # 连接数据库
        conn = pymysql.connect(**self.config)
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
        sql = """delete from customer WHERE name = %s and tele =%s"""
        cursor.execute(sql,(name,tele))
        conn.commit()
        cursor.close()  # 关闭光标对象
        conn.close()  # 关闭数据库连接

    def insert(self, name,tele,data):  # 添加数据
        # 连接数据库
        conn = pymysql.connect(**self.config)
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
        sql = """insert into customer (name,tele,age, job,marital,education,`default`,balance,housing,loan,result) values
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        data.insert(0, name)
        data.insert(1, tele)
        cursor.execute(sql, data)
        conn.commit()
        cursor.close()  # 关闭光标对象
        conn.close()  # 关闭数据库连接

# a = Database()
# a.createTable()
# a.wrinteInDatabase()
# a.insert('a','123456',['40', 'management', 'married', 'tertiary', 'no', '1940', 'no', 'yes', 'no'])
# b = a.select('a','123456')
# print(b)
# c = a.showAll()
# print(c)
# a.update(2, [0, 'management', 'married', 'tertiary', 'no', 10000, 'no', 'yes', 'no'])
# a.delete(2)
# a.insert(4521, [40, 'management', 'married', 'tertiary', 'no', 1940, 'no', 'yes', 'no'])
