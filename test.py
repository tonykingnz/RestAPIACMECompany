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
    def testCreateStore(self):
        it = 0
        with open('outputCreateStoreTest.json') as outputCreateStoresFile:
            storesOutput = json.load(outputCreateStoresFile)
            with open('inputCreateStoreTest.json') as inputCreateStoresFile:
                storesInput = json.load(inputCreateStoresFile)
                for store in storesInput['stores']:
                    self.assertEqual(str(create(store)), storesOutput['stores'][it]['response'], "Store creation failed!")
                    it += 1
                    
#    def testListStore(self):
#        it = 0
#        with open('outputListStoreTest.json') as outputListStoresFile:
#            storesOutput = json.load(outputListStoresFile)
#            with open('inputListStoreTest.json') as inputListStoresFile:
#                storesInput = json.load(inputListStoresFile)
#                for store in storesInput['stores']:
#                    self.assertEqual(str(create(store)), storesOutput['stores'][it]['response'], "List store failed!")
#                    it += 1

#    def testDetailStore(self):
#
#        self.assertEqual(detailStore, EXPECTEDOUTPUTDETAILSTORE, "Detail Store failed")
#
#    def testUpdateStore(self):
#
#        self.assertEqual(updateStore, EXPECTEDOUTPUTUPDATESTORE, "Update Store failed")
#
#    def testRemoveStore(self):
#
#        self.assertEqual(removeStore, EXPECTEDOUTPUTREMOVESTORE, "Remove Store failed")

if __name__ == '__main__':
    unittest.main()
