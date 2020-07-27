#!/usr/bin/env python3
import connexion
from datetime import datetime, timedelta
import logging

from connexion import NoContent

# our memory-only store storage
STORES = {}
ORDERS = {}
STORE_ID = 0
ORDER_ID = 0

def list(limit, storeAddress=None):
    return {"stores": [store for store in STORES.values() if not storeAddress or store['address'] == storeAddress][:limit]}

def create(store):
    global STORE_ID
    time = datetime.utcnow()
#    time.strftime('%m/%d/%Y')
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
        
def order(orderId):
    order = ORDERS.get(orderId)
    return order or ('Not found', 404)

def createOrder(order):
    global ORDER_ID
    ORDER_ID += 1
    order['id'] = ORDER_ID
    ORDERS[ORDER_ID] = order
    return ('No Content', 201)

def refund(orderId):
    if orderId in ORDERS:
        date = ORDERS[orderId].get('confirmationDate')
        orderDate = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
        dateNow = datetime.utcnow()
        refundPeriod = orderDate + timedelta(days=10)
#        refundPeriod = str(refundPeriod)

        if refundPeriod >= dateNow:
#            ORDERS[orderId].update('status') = 'refunded'
            logging.info('Refunding Order %s..', orderId)
            del ORDERS[orderId]
            return ('Refund period of 10 days paced, sorry', 404)
        else:
            return NoContent, 404
            
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

