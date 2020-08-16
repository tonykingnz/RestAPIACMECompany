#!/usr/bin/env python3
import connexion
from datetime import datetime, timedelta
import logging

from connexion import NoContent


from service.store_service.store import listStore
from service.store_service.store import createStore
from service.store_service.store import updateStore
from service.store_service.store import detailStore
from service.store_service.store import removeStore
from service.order_service.order import listOrders
from service.order_service.order import createOrders
from service.order_service.order import updateOrders
from service.order_service.order import detailOrders
from service.order_service.order import refundOrder
from service.order_service.order import refundItemOrder
from service.order_service.order import createPayments
from service.order_service.order import paymentInformations


ORDERS = {}
PAYMENTS = {}
ORDER_ID = 0

#Store
def list(storeAddress=None):
    return (listStore(storeAddress))

def create(store):
    return (createStore(store))
    
def detail(storeId):
    return (detailStore(storeId))

def update(store, storeId):
    return (updateStore(store, storeId))
    
def remove(storeId):
    return (removeStore(storeId))

#Order
def listOrder(status=None):
    return(listOrders(status))

def createOrder(order):
    return(createOrders(order))

def detailOrder(orderId):
    return(detailOrders(orderId))

def updateOrder(address, orderId):
    return(updateOrders(address, orderId))

def refund(orderId):
    return(refundOrders(orderId))

def refundItem(orderId, orderItemsID):
    return(refundItemOrder(orderId, orderItemsID))

#Payment
def createPayment(orderId, payment):
    return(createPayments(orderId, payment))

def paymentInformation(orderId):
    return(paymentInformations(orderId))

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
