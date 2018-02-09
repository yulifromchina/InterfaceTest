# 增加签名+时间戳

# 对Event接口进行测试
# 发布会查询接口

import unittest
import requests
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data
import time
import hashlib

class GetEventListTest(unittest.TestCase):
    """查询发布会信息"""

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/get_event_list_with_md5/"
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

    # 请求超时
    def test_time_out(self):
        r = requests.get(self.base_url, params={'eid': 1,'sign':self.sign_md5, 'time':'915123661'})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10032)
        self.assertEqual(self.result['message'], 'time out')

    # 认证失败
    def test_sign_error(self):
        r = requests.get(self.base_url, params={'eid': 1,'sign':'1111', 'time':self.client_time})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10034)
        self.assertEqual(self.result['message'], 'sign error')


    # eid查询不存在
    def test_get_event_list_eid_error(self):
        r = requests.get(self.base_url, params={'eid': 100,'sign':self.sign_md5, 'time':self.client_time})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10005)
        self.assertEqual(self.result['message'], 'query result is empty')

    # eid查询成功
    def test_get_event_list_eid_success(self):
        r = requests.get(self.base_url, params={'eid': 1,'sign':self.sign_md5, 'time':self.client_time})
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'success')
        self.assertEqual(self.result['data']['name'], '魅蓝 S6发布会')
        self.assertEqual(self.result['data']['address'], '北京会展中心')

    # 关键字模糊查询成功
    def test_get_event_list_name_find(self):
        r = requests.get(self.base_url, params={'name': '发布会','sign':self.sign_md5, 'time':self.client_time})
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'success')
        self.assertEqual(self.result['data'][0]['name'], '魅蓝 S6发布会')
        self.assertEqual(self.result['data'][0]['address'], '北京会展中心')


if __name__ == '__main__':
    test_data.init_data()
    unittest.main()