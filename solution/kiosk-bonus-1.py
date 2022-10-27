from flask import abort, Flask, jsonify, request

app = Flask(__name__)

ITEMS = [
    'apple',
    'banana',
    'pineapple',
]

CART = {}


@app.get('/kiosk/items')
def get_items():
    return jsonify(ITEMS)


@app.post('/kiosk/cart')
def add_to_cart():
    payload = request.get_json()
    item_name = payload.get('item_name', None)

    if item_name not in ITEMS:
        # Item does not exist.
        abort(404)  # TODO: 400 bad request?

    if item_name in CART:
        CART[item_name]['count'] += 1
    else:
        CART[item_name] = {'count': 1}

    return jsonify(CART)


@app.get('/kiosk/cart')
def view_cart():
    return jsonify(CART)


@app.delete('/kiosk/cart/<item_name>')
def delete_from_cart(item_name):
    try:
        del CART[item_name]
    except KeyError:
        # Item is not in cart.
        abort(404)

    return jsonify(CART)


@app.put('/kiosk/cart/<item_name>')
def update_in_cart(item_name):
    payload = request.get_json()
    count = payload.get('count', None)

    if item_name not in ITEMS:
        # Item does not exist.
        abort(404)  # TODO: 400 bad request?

    if not isinstance(count, int):
        # Count is not a number (bad request).
        abort(400)

    if item_name in CART:
        CART[item_name]['count'] += count
    else:
        CART[item_name] = {'count': count}

    return jsonify(CART)


app.run()
