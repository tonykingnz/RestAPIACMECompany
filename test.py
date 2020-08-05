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


def formatUpdateStore (updateStore):
    updateStore = str(updateStore)
    updateStore = updateStore.replace("<object object at", "")
    updateStore = updateStore.replace("(", "")
    updateStore = updateStore.replace(")", "")
    updateStore = updateStore.replace(" ", "")
    updateStore = updateStore.split(",")
    updateStore = int(updateStore[1])
    return updateStore

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
        with open('outputListFiltredStoreTest.json') as outputListStoresFile:
            storesOutput = json.load(outputListStoresFile)
            self.assertEqual(list(storesOutput['stores'][0]['address']), storesOutput, "List store filtred failed!")
        print("")

#    def testDetailStore(self):
#
#        self.assertEqual(detailStore, EXPECTEDOUTPUTDETAILSTORE, "Detail Store failed")
#
#
#    def testRemoveStore(self):
#
#        self.assertEqual(removeStore, EXPECTEDOUTPUTREMOVESTORE, "Remove Store failed")

if __name__ == '__main__':
    unittest.main()
