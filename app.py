#!/usr/bin/env python3
import connexion
from datetime import datetime, timedelta
import logging

from connexion import NoContent

# our memory-only storage and variables
STORES = {}
ORDERS = {}
PAYMENTS = {}
STORE_ID = 0
ORDER_ID = 0

#Store
def list(storeAddress=None):
    return {"stores": [store for store in STORES.values() if not storeAddress or store['address'] == storeAddress]}

def create(store):
    global STORES
    global STORE_ID
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    store['created'] = time
    STORE_ID += 1
    store['id'] = STORE_ID
    STORES[STORE_ID] = store
    return (STORES[STORE_ID]['id'], 201)
    
def detail(storeId):
    global STORES
    store = STORES.get(storeId)
    return store or ('Not found', 404)

def update(store, storeId):
    global STORES
    exists = storeId in STORES
    if exists:
        store['id'] = storeId
        logging.info('Updating store %s..', storeId)
        STORES[storeId] = store
    return NoContent, (200 if exists else 404)
    
def remove(storeId):
    global STORES
    if storeId in STORES:
        logging.info('Deleting store %s..', storeId)
        del STORES[storeId]
        return NoContent, 204
    else:
        return NoContent, 404
        
#Order
def listOrder(status=None):
    return {"orders": [orders for orders in ORDERS.values() if not status or orders['status'] == status]}
    
def createOrder(order):
    global ORDER_ID
    ORDER_ID += 1
    item_id = 0
    time = datetime.utcnow()
    order['confirmationDate'] = time
    order['id'] = ORDER_ID
    order['status'] = 'PENDING'
    order['paid'] = False
    orderItems = order['orderItems']
    for items in orderItems:
        item_id += 1
        items['itemId'] = item_id
        items['status'] = 'ACTIVE'
    order['orderItems'] = orderItems
    ORDERS[ORDER_ID] = order
    return (ORDERS[ORDER_ID]['id'], 201)

def detailOrder(orderId):
    order = ORDERS.get(orderId)
    return order or ('Not found', 404)

def updateOrder(address, orderId):
    exists = orderId in ORDERS
    if exists:
        order = ORDERS[orderId]
        order['id'] = orderId
        order['address'] = address
        logging.info('Updating order %s..', orderId)
        ORDERS[orderId].update(order)
    return NoContent, (200 if exists else 404)

def refund(orderId):
    if orderId in ORDERS:
        date = ORDERS[orderId].get('confirmationDate')
        orderDate = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S.%f')
        refundPeriod = orderDate + timedelta(days=10)
        dateNow = datetime.utcnow()

        if refundPeriod >= dateNow:
            order = ORDERS[orderId]
            if order['paid'] == True:
                order['status'] = 'CANCELED'
                orderItems = order['orderItems']
                for items in orderItems:
                    items['status'] = 'REFUNDED'
                    order['orderItems'] = orderItems
                ORDERS[orderId] = order
                logging.info('Refunding Order %s..', orderId)
                return ('Order refunded sucesfully', 200)
            else:
                return ('Order not paid. To refund requires a payment', 404)
        else:
            return ('Refund period of 10 days paced, sorry', 404)
    else:
        return ('Order ID is not valid or any other error', 404)

def refundItem(orderId, orderItemsID):
    if orderId in ORDERS:
        date = ORDERS[orderId].get('confirmationDate')
        orderDate = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S.%f')
        refundPeriod = orderDate + timedelta(days=10)
        dateNow = datetime.utcnow()
        if refundPeriod >= dateNow:
            order = ORDERS[orderId]
            if order['paid'] == True:
                orderItems = order['orderItems']
                for items in orderItemsID:
                    try:
                        itemIdNumber = int(items)
                        itemIdNumber -= 1
                        orderStatus = orderItems[itemIdNumber]
                        orderStatus['status'] = 'REFUNDED'
                        orderItems[itemIdNumber] = orderStatus
                    except:
                        return ('Some item ID dont found')
                order['orderItems'] = orderItems
                ORDERS[orderId] = order
                logging.info('Refunding items from the order %s..', orderId)
                return ('Order items refunded sucesfully', 200)
            else:
                return ('Order not paid. Refund requires a payment', 404)
        else:
            return ('Refund period of 10 days paced, sorry', 404)
    else:
        return ('Order ID is not valid or any other error', 404)
        
#Payment
def createPayment(orderId, payment):
    if orderId not in PAYMENTS:
        time = datetime.utcnow()
        payment['idFromOrder'] = orderId
        payment['paymentDate'] = time
        payment['status'] = 'SUBMITED'
        order = ORDERS[orderId]
        order['status'] = 'SUBMITED'
        order['paid'] = True
        ORDERS[orderId] = order
        PAYMENTS[orderId] = payment
        return (PAYMENTS[orderId], 201)
    else:
        return ('Payment already created', 404)

def paymentInformation(orderId):
    payment = PAYMENTS.get(orderId)
    return payment or ('Not found', 404)

#Configurations
logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('swagger.yaml')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=8080, server='gevent')
