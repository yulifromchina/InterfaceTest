# 从django自带的sqlite3更改为了mysql，测试连接情况

import pymysql.cursors

# 连接数据库
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='123456',
                             db='Guest',
                             charset='utf8mb4', #  utf-8最长只支持3个字节，utf8mb4可以支持4个字节，消耗更多空间，但兼容性更好
                             cursorclass=pymysql.cursors.DictCursor
                             )


try :
    # 清除数据（如果执行过用例，可能有残留数据）
    with connection.cursor() as cursor:
        try:
            sql = 'DELETE FROM sign_guest WHERE realname = "sname"'
            cursor.execute(sql)
        except:
            pass

    # 创建一条记录插入数据库中
    with connection.cursor() as cursor:
        sql = 'INSERT INTO sign_guest (realname, phone, email, sign, event_id,create_time) ' \
              'VALUES ("sname",123456,"sname@email.com",0,1,NOW());'
        cursor.execute(sql)
        connection.commit()

    # 读取刚刚创建的记录
    with connection.cursor() as cursor:
        sql = "SELECT realname, phone, email, sign FROM sign_guest WHERE phone = %s"
        cursor.execute(sql,('123456',))
        result = cursor.fetchone()
        print(result)
finally:
        connection.close()

