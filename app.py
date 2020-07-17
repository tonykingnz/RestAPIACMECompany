#!/usr/bin/env python3
import connexion
import datetime
import logging

from connexion import NoContent

# our memory-only store storage
STORES = {}


def list(limit, storeAddress=None):
    return {"stores": [store for store in STORES.values() if not storeAddress or store['storeAddress'] == storeAddress][:limit]}

def create(storeId, store):
#    notExists = storeId not in STORES
#    store['id'] = storeId
#
#    if notExists:
#        logging.info('Creating store %s..', storeId)
#        store['created'] = datetime.datetime.utcnow()
#        STORES[storeId] = store
#    return NoContent, (200 if exists else 201)

def detail(storeId):
    store = STORES.get(storeId)
    return store or ('Not found', 404)

def update(storeId, store):
    exists = storeId in STORES
    if exists:
        logging.info('Updating store %s..', storeId)
        STORES[storeId].update(store)
    else:
        return ('Not found', 404)

def remove(storeId):
    if storeId in STORES:
        logging.info('Deleting store %s..', storeId)
        del STORES[storeId]
        return NoContent, 204
    else:
        return NoContent, 404

logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('openapi.yaml')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=8080, server='gevent')
