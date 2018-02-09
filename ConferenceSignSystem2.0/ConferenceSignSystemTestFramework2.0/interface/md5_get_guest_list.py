# 增加签名+时间戳

# 对Event接口进行测试
# 嘉宾查询接口

import unittest
import requests
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data
import time
import hashlib


class GetGuestTest(unittest.TestCase):
    """嘉宾查询接口"""

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/get_guest_list_with_md5/"
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
        r = requests.get(self.base_url, params={'eid': 1, 'phone': '13618330000','sign':self.sign_md5,
                                                'time':'915123661'})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10032)
        self.assertEqual(self.result['message'], 'time out')


    # 认证失败
    def test_sign_error(self):
        r = requests.get(self.base_url, params={'eid': 1, 'phone': '13618330000','sign':'1111',
                                                'time':self.client_time})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10034)
        self.assertEqual(self.result['message'], 'sign error')

    # eid参数为空
    def test_get_guest_list_eid_null(self):
        r = requests.get(self.base_url, params={'eid': '','sign':self.sign_md5, 'time':self.client_time})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10006)
        self.assertEqual(self.result['message'], 'event id null')

    #eid查询为空
    def test_get_event_list_eid_error(self):
        r = requests.get(self.base_url, params={'eid': 100,'sign':self.sign_md5, 'time':self.client_time})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10005)
        self.assertEqual(self.result['message'], 'query result is empty')

    #eid和phone都不为空，通过联合主键来查找失败
    def test_get_event_list_eid_phone_null(self):
        r = requests.get(self.base_url, params={'eid': 1, 'phone': '10000000000','sign':self.sign_md5, 'time':self.client_time})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10005)
        self.assertEqual(self.result['message'], 'query result is empty')

    #查找成功
    def test_get_event_list_eid_phone_success(self):
        r = requests.get(self.base_url, params={'eid': 1, 'phone': '13618330000','sign':self.sign_md5, 'time':self.client_time})
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'success')
        self.assertEqual(self.result['data']['realname'], 'max')
        self.assertEqual(self.result['data']['phone'], '13618330000')

if __name__ == '__main__':
    test_data.init_data()
    unittest.main()