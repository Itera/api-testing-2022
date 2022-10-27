from flask import Flask, jsonify, request

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
    del CART[item_name]
    return jsonify(CART)


app.run()
