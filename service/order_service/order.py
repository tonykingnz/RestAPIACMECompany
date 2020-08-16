import enum

import connexion
from datetime import datetime, timedelta
import logging

from connexion import NoContent

# our memory-only storage and variables
ORDERS = {}
ORDER_ID = 0
PAYMENTS = {}
#Order

def listOrders(status=None):
    global ORDERS
    return {"orders": [orders for orders in ORDERS.values() if not status or orders['status'] == status]}
    
def createOrders(order):
    global ORDERS
    global ORDER_ID
    ORDER_ID += 1
    item_id = 0
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

def detailOrders(orderId):
    global ORDERS
    order = ORDERS.get(orderId)
    return order or ('Not found', 404)

def updateOrders(address, orderId):
    global ORDERS
    exists = orderId in ORDERS
    if exists:
        order = ORDERS[orderId]
        order['id'] = orderId
        order['address'] = address
        logging.info('Updating order %s..', orderId)
        ORDERS[orderId] = order
    return NoContent, (200 if exists else 404)

def refundOrder(orderId):
    global ORDERS
    if orderId in ORDERS:
        date = ORDERS[orderId].get('confirmationDate')
        orderDate = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
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

def refundItemOrder(orderId, orderItemsID):
    global ORDERS
    if orderId in ORDERS:
        date = ORDERS[orderId].get('confirmationDate')
        orderDate = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
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
def createPayments(orderId, payment):
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
        return (PAYMENTS[orderId]['id'], 201)
    else:
        return ('Payment already created', 404)

def paymentInformations(orderId):
    payment = PAYMENTS.get(orderId)
    return payment or ('Not found', 404)
