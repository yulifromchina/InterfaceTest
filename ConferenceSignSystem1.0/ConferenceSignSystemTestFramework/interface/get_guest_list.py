# 对Event接口进行测试
# 嘉宾查询接口

import unittest
import requests
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data

class GetGuestTest(unittest.TestCase):
    """嘉宾查询接口"""

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/get_guest_list/"

    def tearDown(self):
        print(self.result)

    # eid参数为空
    def test_get_guest_list_eid_null(self):
        r = requests.get(self.base_url, params={'eid': ''})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10006)
        self.assertEqual(self.result['message'], 'event id null')

    #eid查询为空
    def test_get_event_list_eid_error(self):
        r = requests.get(self.base_url, params={'eid': 100})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10005)
        self.assertEqual(self.result['message'], 'query result is empty')

    #eid和phone都不为空，通过联合主键来查找失败
    def test_get_event_list_eid_phone_null(self):
        r = requests.get(self.base_url, params={'eid': 1, 'phone': '10000000000'})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10005)
        self.assertEqual(self.result['message'], 'query result is empty')

    #查找成功
    def test_get_event_list_eid_phone_success(self):
        r = requests.get(self.base_url, params={'eid': 1, 'phone': '13618330000'})
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'success')
        self.assertEqual(self.result['data']['realname'], 'max')
        self.assertEqual(self.result['data']['phone'], '13618330000')

if __name__ == '__main__':
    test_data.init_data()
    unittest.main()