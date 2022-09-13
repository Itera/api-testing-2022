# Setup

## Install Python if you don't already have it
You can download it from [here](https://www.python.org/downloads/)

Alternativly on windows you can run 

```    
winget install -e --id Python.Python.3
```

It is assumed Python 3.x is available. To check the current version of Python,
run

```
python --version
```

If the default version is 2.x, you should probably run the commands below with
`python3` instead.

## Initial setup

Install dependencies with

```
python -m pip install -r requirements.txt
```

If you're having certificate issues (typically due to a proxy), you could tell
Python to trust the two hosts:

```
python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

## Install postman

See https://www.postman.com/downloads/

# Tasks

To get up and running, create a Flask app by putting the following in `app.py`.

    from flask import Flask

    app = Flask(__name__)

Run the app with

    python -m flask run

This starts your app on port http://localhost:5000 
   
   
### 1. Create a GET endpoint to get a list of available items

Example of a list of items:

    ITEMS = [
        {'id': 0, 'name': 'Bannana'},
        {'id': 1, 'name': 'Apple'},
    ]

The very first endpoint will simply look something like:

    @app.get('/kiosk/items')
    def get_items():
        return jsonify(ITEMS)

### 2. Create a cart POST endpoint to add an item to a shopping cart

You will need to create a cart of some kind, typically a simple array of items:

    CART = [
        {
            'id': item['id'],
            'name': item['name'],
            'count': 1,
        },
        ...
    ]

The id for the item to be added should be found in the request payload:

    @app.post('/kiosk/cart')
    def add_to_cart():
        payload = request.get_json()
        item_id = payload.get('item_id', None)
        ...

Use Postman to test non-GET requests.

### 3. Create a cart GET endpoint to get items in cart

This is easy now, yes? If it's not, look at what you did in the first task ;)

### 4. Create a cart PUT endpoint for updating the amount of an item in the cart

The PUT endpoint should get the _item id_ from the url (as type `int`):

    @app.put('/kiosk/cart/<int:item_id>')
    def modify_count(item_id):
        ...

### 5. Create a cart DELETE endpoint to delete an item from the cart

The DELETE endpoint should also get the item id from the url.

### 6. Create a user endpoint to create a session id tokens

The user endpoint should get first and last name from the body, and return a
_session id_ token (just a random string).

    session_id = secrets.token_urlsafe(TOKEN_SIZE)

Store this session id somewhere, so it may be used for "authentication" later.

### 7. Add session id as requirement in the header to cart endpoints to "secure" them

Add `Session-Id` to the header of all four requests to /kiosk/cart in Postman.

Then, check if `Session-Id` is set in the header in your app:

    session_id = request.headers.get('Session-Id')

If it's not, the user is not authenticated, and you should return a 401
Unauthorized.

    abort(401)

If there _is_ a session id in the header, but it does not exist in the list of
session ids, the user does not have access and a 403 Forbidden should be
returned.

    abort(403)

Finally, use this session id to store one cart per session, so the different
users have their own cart.  Feel free to peek at our implementation from the
solution: [solution/kiosk/cart.py](https://github.com/Itera/api-testing-2022/blob/main/solution/kiosk/carts.py)
