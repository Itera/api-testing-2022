CARTS = {}


def _find(session_id):
    if session_id not in CARTS:
        CARTS[session_id] = {}

    return CARTS[session_id]


def _create_cart_item(item, count):
    return {'id': item['id'], 'name': item['name'], 'count': count}


def get(session_id):
    cart = _find(session_id)
    return list(cart.values())


def add(session_id, item):
    cart = _find(session_id)
    item_id = item['id']
    if item_id in cart:
        cart[item_id]['count'] += 1
    else:
        cart[item_id] = _create_cart_item(item, 1)

    return list(cart.values())


def remove(session_id, item):
    cart = _find(session_id)
    item_id = item['id']
    del cart[item_id]
    return list(cart.values())


def update(session_id, item, count):
    cart = _find(session_id)
    item_id = item['id']
    if item_id in cart:
        cart[item_id]['count'] = count
    else:
        cart[item_id] = _create_cart_item(item, count)

    return list(cart.values())
