#!/usr/bin/env python3
import connexion
import datetime
import logging

from connexion import NoContent

# our memory-only store storage
STORES = {}
STORE_ID = 0

def list(limit, storeAddress=None):
    return {"stores": [store for store in STORES.values() if not storeAddress or store['address'] == storeAddress][:limit]}

def create(store):
    global STORE_ID
    time = datetime.datetime.utcnow()
    time.strftime('%m/%d/%Y')
    store['created'] = time
    STORE_ID += 1
    store['id'] = STORE_ID
    STORES[STORE_ID] = store
    return ('No Content', 201)
    
def detail(storeId):
    store = STORES.get(storeId)
    return store or ('Not found', 404)

def update(store, storeId):
    exists = storeId in STORES
    store['id'] = storeId
    if exists:
        logging.info('Updating store %s..', storeId)
        STORES[storeId].update(store)
    return NoContent, (200 if exists else 404)
    
def remove(storeId):
    if storeId in STORES:
        logging.info('Deleting store %s..', storeId)
        del STORES[storeId]
        return NoContent, 204
    else:
        return NoContent, 404

logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('swagger.yaml')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=8080, server='gevent')
