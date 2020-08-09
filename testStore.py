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
        with open('inputUpdateStoreTest.json') as input_file:
            dataInput = json.load(input_file)
            with open('outputUpdateStoreTest.json') as output_file:
                dataOutput = json.load(output_file)
                for statusCode in dataOutput['stores']:
                    store = dataInput[it]
                    response = update(store, store['id'])
                    statusCode = statusCode['response']
                    self.assertEqual(response[1], statusCode, "Update store failed!")
                    it += 1
               
#    def test03ListNonFiltredStore(self):
#        with open('listStoreTestCase.json') as payloadFile:
#            payload = json.load(payloadFile)
#            inputTest = payload['input']
#            outputTest = payload['output']
#            self.assertEqual(list(inputTest), outputTest, "List store failed!")
#        print("")

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
