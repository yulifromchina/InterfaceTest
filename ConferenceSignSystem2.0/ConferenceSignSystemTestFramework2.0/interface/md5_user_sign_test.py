# 增加签名+时间戳

# 对Event接口进行测试
# 用户签到接口

import unittest
import requests
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data
import time
import hashlib


class UserSignTest(unittest.TestCase):
    """用户签到接口"""

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/user_sign_with_md5/"
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
        payload = {'eid': 1, 'phone': 13618330000,'sign':self.sign_md5, 'time':'915123661'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10032)
        self.assertEqual(self.result['message'], 'time out')

    # 认证失败
    def test_sign_error(self):
        payload = {'eid': 1, 'phone': 13618330000,'sign':'1111', 'time':self.client_time}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10034)
        self.assertEqual(self.result['message'], 'sign error')

    #参数为空
    def test_user_sign_all_null(self):
        payload = {'eid': '', 'phone': '','sign':self.sign_md5, 'time':self.client_time}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10001)
        self.assertEqual(self.result['message'], 'parameter error')

    #eid为空
    def test_user_sign_eid_error(self):
        payload = {'eid': 100, 'phone': 13618330000,'sign':self.sign_md5, 'time':self.client_time}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10006)
        self.assertEqual(self.result['message'], 'event id null')

    #发布会状态关闭
    def test_user_sign_status_close(self):
        payload = {'eid': 3, 'phone': 13618335555,'sign':self.sign_md5, 'time':self.client_time}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10007)
        self.assertEqual(self.result['message'], 'event status is not available')

    #发布会已经开始
    def test_user_sign_time_start(self):
        payload = {'eid': 5, 'phone': 13618336666,'sign':self.sign_md5, 'time':self.client_time}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10009)
        self.assertEqual(self.result['message'], 'event has started')

    #未查询到手机号
    def test_user_sign_phone_error(self):
        payload = {'eid': 1, 'phone': 111111111111,'sign':self.sign_md5, 'time':self.client_time}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10010)
        self.assertEqual(self.result['message'], 'user phone null')

    #通过联合主键查询失败
    def test_user_sign_eid_phone_error(self):
        payload = {'eid': 1, 'phone': 13618331111,'sign':self.sign_md5, 'time':self.client_time}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10011)
        self.assertEqual(self.result['message'], 'user did not participate in the conference')

    #已签到
    def test_user_sign_has_sign_in(self):
        payload = {'eid': 2, 'phone': 13618331111,'sign':self.sign_md5, 'time':self.client_time}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10012)
        self.assertEqual(self.result['message'], 'user has sign in')

    #签到成功
    def test_user_sign_success(self):
        payload = {'eid': 1, 'phone': 13618330000,'sign':self.sign_md5, 'time':self.client_time}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'sign success')


if __name__ == '__main__':
    test_data.init_data()
    unittest.main()