import re
import secrets
from flask import abort, Flask, jsonify, request

app = Flask(__name__)

ITEMS = [
    'apple',
    'banana',
    'pineapple',
]

CART = {}

SESSIONS = {}


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


@app.post('/kiosk/users')
def create_user():
    payload = request.get_json()
    first = payload.get('first_name', '')
    last = payload.get('last_name', '')

    if len(first) == 0 or re.search('[^a-zA-Z0-9 ]', first) is not None:
        # First name is empty, or contains invalid characters.
        abort(400)

    if len(last) == 0 or re.search('[^a-zA-Z0-9 ]', last) is not None:
        # Last name is empty, or contains invalid characters.
        abort(400)

    # Create and save "session".
    session_id = secrets.token_urlsafe(16)  # 16 = token size in bytes

    SESSIONS[session_id] = {
        'first_name': first,
        'last_name': last,
    }

    return jsonify(session_id)


app.run()
