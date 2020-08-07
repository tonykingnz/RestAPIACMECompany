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
               
    def test03ListNonFiltredStore(self):
        with open('outputListNonFiltredStoreTest.json') as outputListStoresFile:
            storesOutput = json.load(outputListStoresFile)
            self.assertEqual(list(), storesOutput, "List store failed!")
        print("")

    def test04ListFiltredStore(self):
        with open('listFiltredStoreTest.json') as listStoresFile:
            stores = json.load(listStoresFile)
            self.assertEqual(list(stores['stores'][0]['address']), stores, "List store filtred failed!")
        print("")

    def test05DetailStore(self):
        print("")
        it = 0
        with open('outputDetailStoreTest.json') as outputDetailStoresFile:
            responses = json.load(outputDetailStoresFile)
            with open('inputDetailStoreTest.json') as inputDetailStoresFile:
                inputDetail = json.load(inputDetailStoresFile)
                for storeId in inputDetail:
                    storeId = storeId['id']
                    response = responses[it]
                    self.assertEqual(str(detail(storeId)), str(response['response']), "Detail store failed!")
                    it += 1
            
        
    def test06RemoveStore(self):
        print("")
        with open('removeStoreTest.json') as removeStoresFile:
            stores = json.load(removeStoresFile)
            stores = stores['stores'][0]
            response = remove(stores['id'])
            self.assertEqual(response[1], 204, "Remove store failed!")
        print("")

if __name__ == '__main__':
    unittest.main()
