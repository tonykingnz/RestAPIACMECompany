import unittest
import json

import connexion
from datetime import datetime, timedelta
import logging

from app import list
from app import create
from app import detail
from app import update
from app import remove

class TestStore(unittest.TestCase):
    def test01CreateStore(self):
        it = 0
        with open('outputCreateStoreTest.json') as outputCreateStoresFile:
            storesOutput = json.load(outputCreateStoresFile)
            with open('inputCreateStoreTest.json') as inputCreateStoresFile:
                storesInput = json.load(inputCreateStoresFile)
                for store in storesInput['stores']:
                    self.assertEqual(str(create(store)), storesOutput['stores'][it]['response'], "Store creation failed!")
                    it += 1
                    
    def test02UpdateStore(self):
        it = 0
        print("")
        with open('updateStoreTestCase.json') as payloadFile:
            payload = json.load(payloadFile)
            inputTest = payload['input']
            outputTest = payload['output']
            for store in inputTest:
                self.assertEqual(update(store, store['id'])[1], outputTest[it]['response'], "Update store failed!")
                it += 1

    def test03ListStore(self):
        it = 0
        with open('listStoreTestCase.json') as payloadFile:
            payload = json.load(payloadFile)
            inputTest = payload['input']
            outputTest = payload['output']
            for listFilter in inputTest:
                self.assertEqual(list(listFilter), outputTest[it], "List store failed!")
                it += 1
        print("")

    def test04DetailStore(self):
        print("")
        it = 0
        with open('detailStoreTestCase.json') as payloadFile:
            payload = json.load(payloadFile)
            inputTest = payload['input']
            outputTest = payload['output']
            for response in outputTest:
                self.assertEqual(str(detail(inputTest[it])), str(response['response']), "Detail store failed!")
                it += 1
            
        
    def test05RemoveStore(self):
        print("")
        with open('removeStoreTestCase.json') as removeStoresFile:
            payload = json.load(removeStoresFile)
            storeId = payload[0]['input']
            statusCode = payload[0]['output']
            response = remove(storeId)
            self.assertEqual(response[1], statusCode, "Remove store failed!")
        print("")

if __name__ == '__main__':
    unittest.main()
