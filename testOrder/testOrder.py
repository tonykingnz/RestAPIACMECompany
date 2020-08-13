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
from app import createPayment
from app import paymentInformation
from app import refund
from app import refundItem

class TestOrder(unittest.TestCase):
    def test01CreateOrder(self):
        print("")
        with open('createOrderTestCase.json') as payloadFile:
            payload = json.load(payloadFile)
            for testCase in payload:
                self.assertEqual(str(createOrder(testCase["input"])), testCase["output"], "Create order failed!")

    def test02UpdateOrder(self):
        print("")
        with open('updateOrderTestCase.json') as payloadFile:
            payload = json.load(payloadFile)
            for testCase in payload:
                self.assertEqual(updateOrder(testCase['input']['address'], testCase['input']['id'])[1], testCase['output'], "Update order failed!")
                print("")

    def test03ListOrder(self):
        print("")
        with open('listOrderTestCase.json') as payloadFile:
            payload = json.load(payloadFile)
            for testCase in payload:
                self.assertEqual(listOrder(testCase['input']), testCase['output'], "List order failed!")

    def test04DetailOrder(self):
        print("")
        with open('detailOrderTestCase.json') as payloadFile:
            payload = json.load(payloadFile)
            for testCase in payload:
                self.assertEqual(str(detailOrder(testCase['input'])), str(testCase['output']), "Detail order failed!")

    def test05CreatePaymentOrder(self):
        print("")
        with open('createPaymenteOrderTestCase.json') as payloadFile:
            payload = json.load(payloadFile)
            for testCase in payload:
                self.assertEqual(str(createPayment(testCase["input"]['id'], testCase["input"])),str(testCase["output"]), "Order refund failed!")

    def test06InfoPaymentOrder(self):
        print("")
        with open('informationPaymenteOrderTestCase.json') as payloadFile:
            payload = json.load(payloadFile)
            for testCase in payload:
                self.assertEqual(str(paymentInformation(testCase["input"])),str(testCase["output"]), "Order refund failed!")

    def test07OrderRefund(self):
        print("")
        with open('orderRefundTestCase.json') as payloadFile:
            payload = json.load(payloadFile)
            for testCase in payload:
                self.assertEqual(str(refund(testCase["input"])),str(testCase["output"]), "Order refund failed!")
                print("")

    def test08ItemRefund(self):
        print("")
        with open('itemRefundTestCase.json') as payloadFile:
            payload = json.load(payloadFile)
            for testCase in payload:
                self.assertEqual(str(refundItem(testCase['input']['orderId'], testCase['input']['itemId'])), testCase['output'], "Item refund failed!")
                print("")
        print("")
if __name__ == '__main__':
    unittest.main()
