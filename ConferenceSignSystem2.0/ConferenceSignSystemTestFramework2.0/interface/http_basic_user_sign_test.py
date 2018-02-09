# 增加http basic 安全认证：客户端使用base64加密“user:password”（requests库的HTTPBasicAuth实现）,服务段进行base64解码认证
# 对Event接口进行测试
# 用户签到接口

import unittest
import requests
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data


class UserSignTest(unittest.TestCase):
    """用户签到接口"""

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/sec_user_sign/"
        self.user_auth = ('admin', 'abc123456')

    def tearDown(self):
        print(self.result)

    def test_auth_null(self):
        """测试auth为空的情况"""
        payload = {'eid': 1, 'phone': 13618330000}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertEqual(self.result['message'], 'auth cannot be null')

    def test_auth_error(self):
        """测试auth错误的情况"""
        payload = {'eid': 1, 'phone': 13618330000}
        r = requests.post(self.base_url, data=payload,auth=('admin','error password'))
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], 'auth fail')

    #参数为空
    def test_user_sign_all_null(self):
        payload = {'eid': '', 'phone': ''}
        r = requests.post(self.base_url, data=payload,auth=self.user_auth)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10001)
        self.assertEqual(self.result['message'], 'parameter error')

    #eid为空
    def test_user_sign_eid_error(self):
        payload = {'eid': 100, 'phone': 13618330000}
        r = requests.post(self.base_url, data=payload,auth=self.user_auth)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10006)
        self.assertEqual(self.result['message'], 'event id null')

    #发布会状态关闭
    def test_user_sign_status_close(self):
        payload = {'eid': 3, 'phone': 13618335555}
        r = requests.post(self.base_url, data=payload,auth=self.user_auth)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10007)
        self.assertEqual(self.result['message'], 'event status is not available')

    #发布会已经开始
    def test_user_sign_time_start(self):
        payload = {'eid': 5, 'phone': 13618336666}
        r = requests.post(self.base_url, data=payload,auth=self.user_auth)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10009)
        self.assertEqual(self.result['message'], 'event has started')

    #未查询到手机号
    def test_user_sign_phone_error(self):
        payload = {'eid': 1, 'phone': 111111111111}
        r = requests.post(self.base_url, data=payload,auth=self.user_auth)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10010)
        self.assertEqual(self.result['message'], 'user phone null')

    #通过联合主键查询失败
    def test_user_sign_eid_phone_error(self):
        payload = {'eid': 1, 'phone': 13618331111}
        r = requests.post(self.base_url, data=payload,auth=self.user_auth)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10011)
        self.assertEqual(self.result['message'], 'user did not participate in the conference')

    #已签到
    def test_user_sign_has_sign_in(self):
        payload = {'eid': 2, 'phone': 13618331111}
        r = requests.post(self.base_url, data=payload,auth=self.user_auth)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10012)
        self.assertEqual(self.result['message'], 'user has sign in')

    #签到成功
    def test_user_sign_success(self):
        payload = {'eid': 1, 'phone': 13618330000}
        r = requests.post(self.base_url, data=payload,auth=self.user_auth)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'sign success')


if __name__ == '__main__':
    test_data.init_data()
    unittest.main()