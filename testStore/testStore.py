import unittest
import json

import connexion
from datetime import datetime, timedelta
import logging

import sys
sys.path.append('../')

from app import list
from app import create
from app import detail
from app import update
from app import remove

class TestStore(unittest.TestCase):
    def test01CreateStore(self):
        with open('createStoreTestCase.json') as payloadFile:
            payload = json.load(payloadFile)
            for testCase in payload:
                self.assertEqual(str(create(testCase["input"])), testCase["output"], "Create store failed!")

    def test02UpdateStore(self):
        print("")
        with open('updateStoreTestCase.json') as payloadFile:
            payload = json.load(payloadFile)
            for testCase in payload:
                self.assertEqual(update(testCase['input'], testCase['input']['id'])[1], testCase['output'], "Update store failed!")

    def test03ListStore(self):
        with open('listStoreTestCase.json') as payloadFile:
            payload = json.load(payloadFile)
            for testCase in payload:
                self.assertEqual(list(testCase['input']), testCase['output'], "List store failed!")
        print("")

    def test04DetailStore(self):
        print("")
        with open('detailStoreTestCase.json') as payloadFile:
            payload = json.load(payloadFile)
            for testCase in payload:
                self.assertEqual(str(detail(testCase['input'])), str(testCase['output']), "Detail store failed!")
            
        
    def test05RemoveStore(self):
        print("")
        with open('removeStoreTestCase.json') as removeStoresFile:
            payload = json.load(removeStoresFile)
            for testCase in payload:
                self.assertEqual(remove(testCase['input'])[1], testCase['output'], "Remove store failed!")
        print("")

if __name__ == '__main__':
    unittest.main()
