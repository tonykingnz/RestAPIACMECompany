import enum

import connexion
from datetime import datetime, timedelta
import logging

from connexion import NoContent

import sys
sys.path.append("../../")
from exceptions import *

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
    return ORDER_ID

def detailOrders(orderId):
    global ORDERS
    if orderId not in ORDERS:
        raise ApiCustomError("Order Id invallid")
    else:
        order = ORDERS.get(orderId)
        return order

def updateOrders(address, orderId):
    global ORDERS
    print(address)
    print(orderId)
    print(ORDERS[orderId])
    if orderId in ORDERS:
        order = ORDERS[orderId]
        order['id'] = orderId
        order['address'] = address
        logging.info('Updating order %s..', orderId)
        ORDERS[orderId] = order
        return NoContent
    else:
        raise ApiCustomError("Order dont found")

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
                return NoContent
            else:
                raise ApiRefundOrderErrorNotPaid('Order not paid. To refund requires a payment', 404)
        else:
            raise ApiRefundOrderErrorPeriodPassed('Refund period of 10 days paced, sorry', 404)
    else:
        raise ApiRefundOrderErrorInvallidID('Order ID is not valid or any other error', 404)

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
                        raise ApiRefundItemOrderErrorInvallidID("Some item ID dont found")
                order['orderItems'] = orderItems
                ORDERS[orderId] = order
                logging.info('Refunding items from the order %s..', orderId)
                return NoContent 
            else:
                raise ApiRefundItemOrderErrorNotPaid("Order not paid. Refund requires a payment")
        else:
            raise ApiRefundItemOrderErrorPeriodPassed("Refund period of 10 days paced, sorry")
    else:
        raise ApiRefundItemOrderErrorInvallidID("Order ID is not valid or any other error")

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
        return PAYMENTS[orderId]['id']
    else:
        raise ApiCustomError("Payment already created")

def paymentInformations(orderId):
    global PAYMENTS
    if orderId not in PAYMENTS:
        raise ApiCustomError("Order Id invallid")
    else:
        payment = PAYMENTS.get(orderId)
        return payment

