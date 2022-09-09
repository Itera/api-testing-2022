CARTS = {}


def get_cart(session_id):
    if session_id not in CARTS:
        CARTS[session_id] = {}

    return CARTS[session_id]


def add_to_cart(session_id, item):
    cart = get_cart(session_id)

    item_id = item['id']
    if item_id in cart:
        cart[item_id]['count'] += 1
    else:
        cart[item_id] = {
            'name': item['name'],
            'count': 1,
        }

    return cart


def update_cart(session_id, item_id, count):
    cart = get_cart(session_id)

    if item_id not in cart:
        raise Exception('Item not found in cart.')

    if count == 0:
        del cart[item_id]
    else:
        cart[item_id]['count'] = count

    return cart
