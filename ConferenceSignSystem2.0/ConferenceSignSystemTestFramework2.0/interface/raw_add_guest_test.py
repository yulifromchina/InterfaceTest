# 对Event接口进行测试
# 添加嘉宾

import unittest
import requests
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data


class AddGuestTest(unittest.TestCase):
    """添加嘉宾"""

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/add_guest/"

    def tearDown(self):
        print(self.result)

    #参数为空
    def test_add_guest_all_null(self):
        payload = {'eid': '', 'realname': '', 'phone': ''}
        r = requests.get(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10001)
        self.assertEqual(self.result['message'], 'parameter error')

    #关联的eid为空
    def test_add_guest_eid_null(self):
        payload = {'eid': 901, 'realname':'someone', 'phone': 13699999999}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10006)
        self.assertEqual(self.result['message'], 'event id null')

    #获取不到发布会开启
    def test_add_guest_status_close(self):
        payload = {'eid': 3, 'realname': 'someone', 'phone': 13699999999}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10007)
        self.assertEqual(self.result['message'], 'event status is not available')

        #发布会人数已满
    def test_add_guest_limit_full(self):
        payload = {'eid': 2, 'realname': 'someone', 'phone': 13699999999}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10008)
        self.assertEqual(self.result['message'], 'event number is full')

    #发布会已经开始
    def test_add_guest_time_start(self):
        payload = {'eid': 5, 'realname': 'someone', 'phone': 13699999999}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10009)
        self.assertEqual(self.result['message'], 'event has started')

    #外键重复(手机号重复和evet_id)
    def test_add_guest_phone_repeat(self):
        payload = {'eid': 1, 'realname': 'someone', 'phone': 13618330000}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10010)
        self.assertEqual(self.result['message'], 'the event guest phone number repeat')

    # 添加成功
    def test_add_guest_success(self):
        payload = {'eid': 1, 'realname': 'someone', 'phone': 13688888888}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'add guest success')


if __name__ == '__main__':
    test_data.init_data()
    unittest.main()