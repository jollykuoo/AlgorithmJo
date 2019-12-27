import pymysql


class Customer:
    def __init__(self):
        self.connection = pymysql.connect(host='localhost', user='root', password='12345678', database='demo')
        self.cursor = self.connection.cursor()
        print("初始化完成！")

    def insert(self):
        sql = 'insert into cus values(%d,%s,%s)' % (4, 'mk', '13900000000')
        self.cursor.execute(sql)
        self.connection.commit()

    def delete(self):
        pass

    def query(self):
        sql = "select * from cus"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        for result in data:
            print("id:%d,name:%s,tele :%s" % (result[0], result[1], result[2]))

    def update(self):
        pass

    def end(self):
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    cus = Customer()
    cus.insert()
    # cus.query()
