#!/usr/bin/env python3
import connexion
from datetime import datetime, timedelta
import logging

from connexion import NoContent

from exceptions import *

from service.store_service.store import *
from service.order_service.order import *


ORDERS = {}
PAYMENTS = {}
ORDER_ID = 0

#Store
def list(storeAddress=None):
    return (listStore(storeAddress))

def create(store):
    try:
        storeId = createStore(store)
        return (storeId, 201)
    except ApiCustomError as e:
        return ("Bad Request", 400)

def detail(storeId):
    try:
        store = detailStore(storeId)
        return store
    except ApiCustomError as e:
        return ("Not found", 404)

def update(store, storeId):
    try:
        response = updateStore(store, storeId)
        return(response, 200)
    except ApiCustomError as e:
        return("Not found", 404)
    
def remove(storeId):
     try:
        response = removeStore(storeId)
        return(response, 204)
     except ApiCustomError as e:
        return("Not found", 404)

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
