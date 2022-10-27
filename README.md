# Setup

## Install Python if you don't already have it

You can download it from [here](https://www.python.org/downloads/)

Alternatively on Windows you can run

    winget install -e --id Python.Python.3

It is assumed Python 3.x is available. To check the current version of Python, run

    python --version

If the default version is 2.x, you should probably run the commands below with
`python3` instead.

## Download project files

If you have git installed, use git to clone project:

    git clone https://github.com/Itera/api-testing-2022.git

or download directly project files
[Download here](https://github.com/Itera/api-testing-2022/archive/refs/heads/main.zip)

## Initial setup

Open a terminal and navigate to the project folder and run these commands.

Install dependencies with

    python -m pip install -r requirements.txt

If you're having certificate issues (typically due to a proxy), you could tell Python to trust the two hosts:

    python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

## Install postman

See https://www.postman.com/downloads/

# Tasks

To get up and running, create a Flask app by putting the following in `kiosk.py`.

    from flask import Flask

    app = Flask(__name__)

    app.run()

Run the app with

    python kiosk.py

This starts your app at http://localhost:5000 (or http://127.0.0.1:5000).

### 1. Create a GET endpoint to get a list of available items

Example of a list of items:

    ITEMS = [
        'Bannana',
        'Apple',
    ]

The very first endpoint will simply return this list (as JSON), and could look something like:

    @app.get('/kiosk/items')
    def get_items():
        return jsonify(ITEMS)

You may use Flasks `jsonify()` utility function to convert objects JSON.

Note that `app.run()` should still be the last line in your script.

### 2. Create a cart POST endpoint to add an item to a shopping cart

You will need to create a cart of some kind, typically a simple dictionary of items with each item's state:

    CART = {
        'Bannana': { 'count': 1 } 
    }

The name for the item to be added should be found in the request payload:

    @app.post('/kiosk/cart')
    def add_to_cart():
        payload = request.get_json()
        item_name = payload.get('item_name', None)
        ...

The request may be read simply by importing Flasks "special" `request` object at the top of your script, which has a
method called `get_json()`.

Tip: use Postman to test non-GET requests.

### 3. Create a cart GET endpoint to get items in cart

This is easy now, yes? If it's not, look at what you did in the first task ;)

### 4. Create a cart DELETE endpoint to delete a specific item from the cart

The DELETE endpoint should get the item name from the url:

    @app.delete('/kiosk/cart/<item_name>')
    def delete_from_cart(item_name):
        ...

It should also return the item that was deleted.

### 5. Create a cart PUT endpoint for updating the amount of an item in the cart

The PUT endpoint should also get the item name from the url:

    @app.put('/kiosk/cart/<item_name>')
    def update_in_cart(item_name):
        ...

## Bonus tasks:

### 1. Error handling

Currently, there is no error handling or checks of any kind. Return appropriate HTTP status codes (mainly 404 Not Found
or 400 Bad Request).

Flask comes with the utility function `abort(status)` to easily abort execution and return a response with the given
status code.

    if item_name not in ITEMS:
        abort(404)

### 2. Create a user endpoint to create a session id token

The user endpoint should get first and last name from the body, and return a
_session id_ token (just a random string).

    session_id = secrets.token_urlsafe(TOKEN_SIZE)

Store this session id somewhere, so it may be used for "authentication" later.

### 3. Add session id to request headers to "secure" cart endpoints

Add `Session-Id` to the header of all four requests to /kiosk/cart in Postman.

Then, check if `Session-Id` is set in the request header in your app:

    session_id = request.headers.get('Session-Id')

If it's not, the user is not _authenticated_, and you should return a 401 Unauthorized.

    abort(401)

If there _is_ a session id in the header, but it does not exist in the list of session ids, the user does not have
_access_, and a 403 Forbidden should be returned.

    abort(403)

### 4. Store one cart per session

Finally, use the session id to store one cart per session, so the different users have their own cart. Feel free to peek
at our implementation from the solution:
[solution/kiosk-bonus-4.py](https://github.com/Itera/api-testing-2022/blob/main/solution/kiosk-bonus-4.py)
