# 封装数据库操作，提供数据插入和清除的操作
import pymysql.cursors   # mysql数据库驱动
import os
import configparser # 解析ini文件

parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parent_path = parent_path.replace('\\','/') # python读取绝对路径使用正斜杠，反斜杠可能带来转义的问题
file_path = parent_path+"/db_config.ini"
#print(file_path)

cf = configparser.ConfigParser()
cf.read(file_path)
host = cf.get("mysqlconf","host")
port = cf.get("mysqlconf","port")
db = cf.get("mysqlconf","db_name")
user = cf.get("mysqlconf","user")
password = cf.get("mysqlconf","password")

class DB(object):

    def __init__(self):
        try:
            # 连接数据库
            self.connection = pymysql.connect(host=host,
                                              user=user,
                                              password=password,
                                              db=db,
                                              charset='utf8mb4',
                                              cursorclass=pymysql.cursors.DictCursor)
        except pymysql.err.OperationalError as e:
            print("MySQL Error %d : %s" % (e.args[0],e.args[1]))

        # 清空表
    def clear(self,table_name):
        sql = "delete from " + table_name + ";"
        with self.connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;") # 去掉外键检查，避免由于外键约束导致无法删除的情况
            cursor.execute(sql)
        self.connection.commit()

        # 插入数据表
    def insert(self, table_name, table_data):
            # table_data是json数据
        for key in table_data:
            table_data[key] = "'"+str(table_data[key]) +"'"
        key = ','.join(table_data.keys())
        value = ','.join(table_data.values())
        sql = "INSERT INTO "+table_name+" (" + key+ ") VALUES ("+value+ ")"
        #print(sql)

        with self.connection.cursor() as cursor:
            cursor.execute(sql)

        self.connection.commit()

    # 关闭数据库
    def close(self):
        self.connection.close()

    # 清空数据库表并插入测试数据
    def init_data(self,datas):
        for table,data in datas.items():
            self.clear(table)
            for d in data:
                self.insert(table,d)
        self.close()


if __name__ == '__main__':
    db=DB()
    table_name="sign_event"
    data={'id':111,'name':'华为','`limit`':2000,'status':1,'address':'北京会展中心',
          'start_time':'2019-01-01 00:00:00','create_time':'2018-01-01 00:00:00'}
    db.clear(table_name)
    db.insert(table_name, data)
    db.close()
