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
        with open('outputCreateStoreTest.json') as outputCreateStoresFile:
            storesOutput = json.load(outputCreateStoresFile)
            count = 0
            with open('inputCreateStoreTest.json') as inputCreateStoresFile:
                storesInput = json.load(inputCreateStoresFile)
                for storeInput in storesInput['stores']:
                    createStore = create(storeInput)
                    createStore = str(createStore)
                    createStoreEdit = createStore.replace('(', '')
                    createStoreEdit = createStoreEdit.split(" 'created': ", 1)
                    createStore = createStoreEdit[0]
                    idStore = createStoreEdit[1]
                    idStore = idStore.split("'id'", 1)
                    idStoreEdit = idStore[1]
                    createStore += " 'id'"
                    createStore += idStoreEdit
                    status = idStoreEdit
                    status = status.split("}", 1)
                    statusEdit = status[1]
                    createStore = createStore.replace(statusEdit, '')
                    stores = storesOutput['stores'][count]
                    store = stores['store']
                    body = store['body']
                    count += 1
                    self.assertEqual(str(createStore), str(body), "Store creation failed")
                    

#    def testListStore(self):
#        with open('outputListStoreTest.json') as outputListStoresFile:
#            listOutput = json.load(outputListStoresFile)
#            listStoreNoFilter = list()
#            listStoreNoFilter = str(listStoreNoFilter)
#            listStoreNoFilter = listStoreNoFilter.replace('(', '')
#            print(listStoreNoFilter)
#            body = listOutput['listComplete']
#            self.assertEqual(str(listStoreNoFilter), str(body), "List store without filter failed")
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
