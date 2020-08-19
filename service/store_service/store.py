import enum

import connexion
from datetime import datetime, timedelta
import logging

from connexion import NoContent

import sys
sys.path.append("../../")
from exceptions import *

# our memory-only storage and variables
STORES = {}
STORE_ID = 0

#Store
def listStore(storeAddress=None):
    return {"stores": [store for store in STORES.values() if not storeAddress or store['address'] == storeAddress]}

def createStore(store):
    global STORES
    global STORE_ID
    for item in STORES.values():
        if item['name'] == store['name']:
            raise ApiCustomError("Store name must not be duplicated")
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    store['created'] = time
    STORE_ID += 1
    store['id'] = STORE_ID
    STORES[STORE_ID] = store
    return STORE_ID

def detailStore(storeId):
    global STORES
    if storeId not in STORES:
        raise ApiCustomError("Store Id invallid")
    else:
        store = STORES.get(storeId)
        return store

def updateStore(store, storeId):
    global STORES
    if storeId in STORES:
        store['id'] = storeId
        logging.info('Updating store %s..', storeId)
        STORES[storeId] = store
        return NoContent
    else:
        raise ApiCustomError("Store dont found")

def removeStore(storeId):
    global STORES
    if storeId in STORES:
        logging.info('Deleting store %s..', storeId)
        del STORES[storeId]
        return NoContent
    else:
        raise ApiCustomError("Store dont found")
