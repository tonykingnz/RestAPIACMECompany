def storeList(storeAddress=None):
    body = {"stores": [store for store in STORES.values() if not storeAddress or store['address'] == storeAddress]}

def storeCreate(store):
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
