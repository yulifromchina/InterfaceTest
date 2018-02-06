import sys
import os
sys.path.append('../db_fixture')
from mysql_db import DB



# 测试数据
datas = {
    'sign_event':[
        {'id':1,'name':'魅蓝 S6发布会','`limit`':2000,'status':1,
         'address':'北京会展中心','start_time':'2019-01-01 00:00:00','create_time':'2018-01-01 00:00:00'},
        {'id': 2, 'name': '可参加人数为0', '`limit`': 0, 'status': 1,
         'address': '北京会展中心', 'start_time': '2019-01-01 00:00:00', 'create_time': '2018-01-01 00:00:00'},
        {'id': 3, 'name': '当前状态为0关闭', '`limit`': 2000, 'status': 0,
         'address': '北京会展中心', 'start_time': '2017-01-01 00:00:00', 'create_time': '2018-01-01 00:00:00'},
        {'id': 4, 'name': '发布会已结束', '`limit`': 2000, 'status': 1,
         'address': '北京会展中心', 'start_time': '2019-01-01 00:00:00', 'create_time': '2018-01-01 00:00:00'},
        {'id': 5, 'name': '魅蓝 Note6', '`limit`': 2000, 'status': 1,
         'address': '北京会展中心', 'start_time': '2018-01-01 00:00:00', 'create_time': '2018-01-01 00:00:00'},
    ],
    'sign_guest':[
        {'id':1,'realname':'max','phone':13618330000,'email':'max@email.com',
         'sign':0,'event_id':1,'create_time': '2018-01-01 00:00:00'},
        {'id': 2, 'realname': 'hasSigned', 'phone': 13618331111, 'email': 'hasSigned@email.com',
         'sign': 1, 'event_id': 2, 'create_time': '2018-01-01 00:00:00'},
        {'id': 3, 'realname': 'caroline', 'phone': 13618332222, 'email': 'caroline@email.com',
         'sign': 0, 'event_id': 1, 'create_time': '2018-01-01 00:00:00'},
        {'id': 4, 'realname': 'matthew', 'phone': 13618334444, 'email': 'matthew@email.com',
         'sign': 0, 'event_id': 2, 'create_time': '2018-01-01 00:00:00'},
        {'id': 5, 'realname': 'susan', 'phone': 13618335555, 'email': 'susan@email.com',
         'sign': 0, 'event_id': 3, 'create_time': '2018-01-01 00:00:00'},
        {'id': 6, 'realname': 'sufei', 'phone': 13618336666, 'email': 'sufei@email.com',
         'sign': 0, 'event_id': 5, 'create_time': '2018-01-01 00:00:00'},
    ],
}


# 插入数据
def init_data():
    DB().init_data(datas)

if __name__=="__main__":
    init_data()