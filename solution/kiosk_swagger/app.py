import re
from flask import abort, Flask, request
from flask_restx import Api, fields, marshal_with, Resource
from kiosk_swagger import carts, items, session

app = Flask(__name__)
api = Api(app)
ns = api.namespace('Kiosk', path='/kiosk')

authHeader = api.parser()
authHeader.add_argument('Session-Id', location='headers')

itemModel = api.model('Item', {
    'id': fields.Integer,
    'name': fields.String,
})

cartItemModel = ns.inherit('CartItem', itemModel, {
    'count': fields.Integer,
})


@ns.route('/items')
class Items(Resource):
    @ns.doc(description='Get a list of all available items.')
    @ns.response(200, 'Success', [itemModel])
    def get(self):
        return items.list_items()


@ns.route('/users')
class Users(Resource):
    @ns.doc(description='Create a new user session.')
    @ns.expect(ns.model('CreateUserRequest', {
        'first_name': fields.String(default='Tom'),
        'last_name': fields.String(default='Testersen'),
    }))
    @ns.response(200, 'Success', fields.String)
    @ns.response(400, 'Invalid first or last name given')
    def post(self):
        payload = request.get_json()
        first = payload.get('first_name', '')
        last = payload.get('last_name', '')

        if len(first) == 0 or re.search('[^a-zA-Z0-9 \\-]', first) is not None:
            abort(400)

        if len(last) == 0 or re.search('[^a-zA-Z0-9 \\-]', last) is not None:
            abort(400)

        return session.create_session(first, last)


@ns.route('/cart')
@ns.expect(authHeader)
class Cart(Resource):
    @ns.doc(description='Get items in cart.')
    @ns.response(200, 'Success', [cartItemModel])
    @ns.response(401, 'No Session-Id header')
    @ns.response(403, 'Invalid Session-Id header')
    def get(self):
        session_id = _get_session_id()
        return carts.get_cart(session_id)

    @ns.doc(description='Add item to cart.')
    @ns.expect(ns.model('AddToCartRequest', {
        'item_id': fields.Integer,
    }))
    @ns.response(200, 'Success', [cartItemModel])
    @ns.response(401, 'No Session-Id header')
    @ns.response(403, 'Invalid Session-Id header')
    @ns.response(404, 'Item not found')
    def post(self):
        session_id = _get_session_id()

        payload = request.get_json()
        item_id = payload.get('item_id', None)

        try:
            item = items.get_item(item_id)
        except:
            abort(404)

        return carts.add_to_cart(session_id, item)


@ns.route('/cart/<int:item_id>')
@ns.expect(authHeader)
class CartItem(Resource):
    @ns.doc(description='Update the amount of an item in cart.')
    @ns.expect(ns.model('UpdateCartRequest', {
        'count': fields.Integer,
    }))
    @ns.response(200, 'Success', [cartItemModel])
    @ns.response(401, 'No Session-Id header')
    @ns.response(403, 'Invalid Session-Id header')
    @ns.response(404, 'Item not found in cart')
    def put(self, item_id):
        session_id = _get_session_id()

        payload = request.get_json()
        count = payload.get('count', None)

        try:
            return carts.update_cart(session_id, item_id, count)
        except:
            abort(404)

    @ns.doc(description='Delete an item from cart.')
    @ns.response(200, 'Success', [cartItemModel])
    @ns.response(401, 'No Session-Id header')
    @ns.response(403, 'Invalid Session-Id header')
    @ns.response(404, 'Item not found in cart')
    def delete(self, item_id):
        session_id = _get_session_id()

        try:
            return carts.update_cart(session_id, item_id, 0)
        except:
            abort(404)


def _get_session_id():
    session_id = request.headers.get('Session-Id')

    if session_id is None:
        abort(401)

    if not session.check_session_id(session_id):
        abort(403)

    return session_id
