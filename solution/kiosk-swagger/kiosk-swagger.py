from flask import abort, Flask, request
from flask_restx import Api, fields, Resource

import carts
import items
import sessions

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
        return items.list()


@ns.route('/cart')
@ns.expect(authHeader)
class Cart(Resource):
    @ns.doc(description='Get items in cart.')
    @ns.response(200, 'Success', [cartItemModel])
    @ns.response(401, 'No Session-Id header')
    @ns.response(403, 'Invalid Session-Id header')
    def get(self):
        session_id = check_session()
        cart = carts.get(session_id)
        return cart

    @ns.doc(description='Add item to cart.')
    @ns.expect(ns.model('AddToCartRequest', {
        'item_id': fields.Integer,
    }))
    @ns.response(200, 'Success', [cartItemModel])
    @ns.response(401, 'No Session-Id header')
    @ns.response(403, 'Invalid Session-Id header')
    @ns.response(404, 'Item not found')
    def post(self):
        session_id = check_session()

        payload = request.get_json()
        item_id = payload.get('item_id', None)

        item = items.get(item_id)
        if item is None:
            # Item does not exist.
            abort(400)  # TODO: 400 bad request?

        cart = carts.add(session_id, item)
        return cart


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
        session_id = check_session()

        payload = request.get_json()
        count = payload.get('count', None)

        if not isinstance(count, int):
            # Count is not a number (bad request).
            abort(400)

        item = items.get(item_id)
        if item is None:
            # Item does not exist.
            abort(404)  # TODO: 400 bad request?

        cart = carts.update(session_id, item, count)
        return cart

    @ns.doc(description='Delete an item from cart.')
    @ns.response(200, 'Success', [cartItemModel])
    @ns.response(401, 'No Session-Id header')
    @ns.response(403, 'Invalid Session-Id header')
    @ns.response(404, 'Item not found in cart')
    def delete(self, item_id):
        session_id = check_session()
        item = items.get(item_id)
        try:
            cart = carts.remove(session_id, item)
            return cart
        except KeyError:
            # Item is not in cart.
            abort(404)


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
        first = payload.get('first_name', None)
        last = payload.get('last_name', None)

        try:
            session_id = sessions.create(first, last)
            return session_id
        except:
            abort(400)


def check_session():
    session_id = request.headers.get('Session-Id')

    if session_id is None:
        abort(401)

    if not sessions.is_valid(session_id):
        abort(403)

    return session_id


app.run()
