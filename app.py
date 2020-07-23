#!/usr/bin/env python3
import connexion
from datetime import datetime, timedelta
import logging

from connexion import NoContent

# our memory-only store storage
STORES = {}
ORDERS = {}
PAYMENTS = {}
STORE_ID = 0
ORDER_ID = 0

def list(limit, storeAddress=None):
    return {"stores": [store for store in STORES.values() if not storeAddress or store['address'] == storeAddress][:limit]}

def create(store):
    global STORE_ID
    time = datetime.utcnow()
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
        
def listOrder(status=None):
    return {"orders": [orders for orders in ORDERS.values() if not status or orders['status'] == status]}
    
def createOrder(order):
    global ORDER_ID
    ORDER_ID += 1
#    time = datetime.utcnow() #should use this instead of confimationDate? Or should use booth. Must update swagger to use
#    order['created'] = time
    order['id'] = ORDER_ID
    ORDERS[ORDER_ID] = order
    return ('No Content', 201)

def detailOrder(orderId):
    order = ORDERS.get(orderId)
    return order or ('Not found', 404)

def updateOrder(order, orderId):
    exists = orderId in ORDERS
    order['id'] = orderId
    if exists:
        logging.info('Updating order %s..', orderId)
        ORDERS[orderId].update(order)
    return NoContent, (200 if exists else 404)
#
#    if orderId in ORDERS:
#        date = ORDERS[orderId].get('confirmationDate')
#        orderDate = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
#        dateNow = datetime.utcnow()
#        refundPeriod = orderDate + timedelta(days=10)
#
#        if refundPeriod >= dateNow:
##fix it      order = ORDERS[orderId].update('status') = 'updated+datenow+ORDERS[orderId].get('status)'
#            logging.info('Updating order %s..', orderId)
#            ORDERS[orderId].update(order)
#            return (NoContent, 200)
#
#        else:
#            return NoContent, 404
#
#
#
#    else:
#        return NoContent, 404

#should only allow change before 10 days. If allowed later, can change the confimation date and refund the order any time.

def refund(orderId):
    if orderId in ORDERS:
        date = ORDERS[orderId].get('confirmationDate')
        orderDate = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
        dateNow = datetime.utcnow()
        refundPeriod = orderDate + timedelta(days=10)

        if refundPeriod >= dateNow:
#fix it            order = ORDERS[orderId].update('status') = 'refunded'
            logging.info('Refunding Order %s..', orderId)
            del ORDERS[orderId]
            return NoContent, 204
        else:
            return ('Refund period of 10 days paced, sorry', 404)
            
    else:
        return NoContent, 404
        
def createPayment(orderId, payment):
#    time = datetime.utcnow() #should use this instead of confimationDate? Or should use booth. Must update swagger to use
#    order['created'] = time
    payment['idFromOrder'] = orderId
    PAYMENTS[orderId] = payment
    return ('No Content', 201)

def paymentInformation(orderId):
    payment = PAYMENTS.get(orderId)
    return payment or ('Not found', 404)
    
def updatePayment(orderId, payment):
    exists = orderId in ORDERS
    payment['idFromOrder'] = orderId
    if exists:
        logging.info('Updating payment for order with ID: %s..', orderId)
        PAYMENTS[orderId].update(payment)
    return NoContent, (200 if exists else 404)
    
        
logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('swagger.yaml')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=8080, server='gevent')

