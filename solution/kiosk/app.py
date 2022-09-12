import re
from flask import abort, Flask, jsonify, request
from kiosk import carts, items, session

app = Flask(__name__)


@app.get('/kiosk/items')
def get_items():
    return jsonify(items.list_items())


@app.post('/kiosk/users')
def create_user():
    payload = request.get_json()
    first = payload.get('first_name', '')
    last = payload.get('last_name', '')

    if len(first) == 0 or re.search('[^a-zA-Z0-9 ]', first) is not None:
        abort(400)

    if len(last) == 0 or re.search('[^a-zA-Z0-9 ]', last) is not None:
        abort(400)

    return jsonify(session.create_session(first, last))


@app.get('/kiosk/cart')
def view_cart():
    session_id = _get_session_id()
    return jsonify(carts.get_cart(session_id))


@app.post('/kiosk/cart')
def add_to_cart():
    session_id = _get_session_id()

    payload = request.get_json()
    item_id = payload.get('item_id', None)

    try:
        item = items.get_item(item_id)
    except:
        abort(404)

    return jsonify(carts.add_to_cart(session_id, item))


@app.put('/kiosk/cart/<int:item_id>')
def modify_count(item_id):
    session_id = _get_session_id()

    payload = request.get_json()
    count = payload.get('count', None)

    try:
        return jsonify(carts.update_cart(session_id, item_id, count))
    except:
        abort(404)


@app.delete('/kiosk/cart/<int:item_id>')
def delete_from_cart(item_id):
    session_id = _get_session_id()

    try:
        return jsonify(carts.update_cart(session_id, item_id, 0))
    except:
        abort(404)


def _get_session_id():
    session_id = request.headers.get('Session-Id')

    if session_id is None:
        abort(401)

    if not session.check_session_id(session_id):
        abort(403)

    return session_id
