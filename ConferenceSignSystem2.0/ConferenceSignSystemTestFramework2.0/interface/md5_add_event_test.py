# 增加签名+时间戳

# 对Event接口进行测试
# 添加发布会

import unittest
import requests
import os
import sys
# 动态方法获取上一级目录，insert(0,parentdir)确保优先搜索该路径
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data
import time
import hashlib

class AddEventTest(unittest.TestCase):
    """添加发布会"""

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/add_event_with_md5/"
        self.secret_key = '&cfssystem'

        now_time = time.time()
        self.client_time = str(now_time).split('.')[0]
        md5 = hashlib.md5()
        sign_str = self.client_time + self.secret_key
        sign_bytes_utf8 = sign_str.encode(encoding='utf-8')
        md5.update(sign_bytes_utf8)
        self.sign_md5 = md5.hexdigest()

    def tearDown(self):
        print(self.result)


    def test_add_event_all_null(self):
        """所有参数为空的情况"""
        payload = {'eid':'','limit':'','address':'','start_time':'','name':'','status':'',
                   'sign':self.sign_md5,'time':self.client_time}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'],10001)
        self.assertEqual(self.result['message'],'parameter error')

    def test_add_event_md5_error(self):
        """md5错误的情况"""
        payload = {'eid': 1, 'name': '某发布会', 'limit': 2000, 'address': "成都会展中心",
                   'start_time': '2020-01-01 00:00:00','status':1,'sign':'111111','time':self.client_time}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10034)
        self.assertEqual(self.result['message'], 'sign error')

    def test_add_event_timeout(self):
        """超时的情况"""
        payload = {'eid': 1, 'name': '某发布会', 'limit': 2000, 'address': "成都会展中心",
                   'start_time': '2020-01-01 00:00:00','status':1,'sign':self.sign_md5,'time':'915123661'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10032)
        self.assertEqual(self.result['message'], 'time out')

    def test_add_event_eid_exist(self):
        """id已经存在的情况"""
        payload = {'eid': 1, 'name': '某发布会', 'limit': 2000, 'address': "成都会展中心",
                   'start_time': '2020-01-01 00:00:00','status':1,'sign':self.sign_md5,'time':self.client_time}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10002)
        self.assertEqual(self.result['message'], 'event id already exists')

    def test_add_event_name_exist(self):
        """名称已经存在的情况"""
        payload = {'eid': 11, 'name': '魅蓝 S6发布会', 'limit': 2000, 'address': "成都会展中心",
                   'start_time': '2017','status':1,'sign':self.sign_md5,'time':self.client_time}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10003)
        self.assertEqual(self.result['message'], 'event name already exists')

    def test_add_event_data_type_error(self):
        """日期格式错误的情况"""
        payload = {'eid': 11, 'name': '某发布会', 'limit': 2000, 'address': "成都会展中心",
                   'start_time': '2020','status':1,'sign':self.sign_md5,'time':self.client_time}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10004)
        self.assertIn('start_time format error', self.result['message'])

    def test_add_event_success(self):
        """添加成功"""
        payload = {'eid': 11, 'name': '魅族PRO 7发布会', 'limit': 2000, 'address': "成都会展中心",
                   'start_time': '2017-05-10 12:00:00','status':1,'sign':self.sign_md5,'time':self.client_time}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'add event success')


if __name__=="__main__":
    test_data.init_data()
    unittest.main()
