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
        print("")
        with open('inputUpdateStoreTest.json') as input_file:
           data = json.load(input_file)
           for store in data:
               response = update(store, store['id'])
               self.assertEqual(response[1], 200, "Update store failed!")
               
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
        with open('detailStoreTest.json') as detailStoresFile:
            stores = json.load(detailStoresFile)
            stores = stores['stores'][0]
            self.assertEqual(detail(stores['id']), stores, "Detail store failed!")
            
        
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
