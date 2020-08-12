import unittest
import json

import connexion
from datetime import datetime, timedelta
import logging

import sys
sys.path.append('../')

from app import listOrder
from app import createOrder
from app import detailOrder
from app import updateOrder

class TestStore(unittest.TestCase):
    def test01CreateOrder(self):
        it = 0
        with open('createOrderTestCase.json') as payloadFile:
            payload = json.load(payloadFile)
            for testCase in payload:
                self.assertEqual(str(createOrder(testCase["input"])), testCase["output"], "Create order failed!")

    def test02UpdateOrder(self):
        print("")
        with open('updateOrderTestCase.json') as payloadFile:
            payload = json.load(payloadFile)
            for testCase in payload:
                self.assertEqual(updateOrder(testCase['input'], testCase['input']['id'])[1], testCase['output'], "Update order failed!")

    def test03ListOrder(self):
        with open('listOrderTestCase.json') as payloadFile:
            payload = json.load(payloadFile)
            for testCase in payload:
                self.assertEqual(listOrder(testCase['input']), testCase['output'], "List order failed!")
        print("")

    def test04DetailOrder(self):
        print("")
        with open('detailOrderTestCase.json') as payloadFile:
            payload = json.load(payloadFile)
            for testCase in payload:
                self.assertEqual(str(detailOrder(testCase['input'])), str(testCase['output']), "Detail order failed!")

if __name__ == '__main__':
    unittest.main()
