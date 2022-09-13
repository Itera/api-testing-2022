# Setup:
## Install pyton if you dont already have it:

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
    
    https://www.postman.com/downloads/
  

# Tasks:

### 1. Create a get enpoint to get a list of availble items  
 List of items example: 

    ITEMS = [
        {'id': 0, 'name': 'Bannana'},
        {'id': 1, 'name': 'Apple'},
    ]

Code example:

    @app.get('/kiosk/items')
    def get_items():
        return jsonify(ITEMS)

### 2. Create a cart POST api to add an item to you shopping cart
You will need to create a cart of some kind, a simple array of items:
    
    {
        'id': item['id'],
        'name': item['name'],
        'count': 1,
    } 
Or you can steal our implentation from the solution: [solution/kiosk/cart.py](https://github.com/Itera/api-testing-2022/blob/main/solution/kiosk/carts.py)

### 3. Create a cart GET enpoint to get items in cart
  
### 4. Create a cart PUT endpoint for updating amount of an item in the cart
The put endpoint should get item_id from the url:

    @app.put('/kiosk/cart/<int:item_id>')
    def modify_count(item_id):
  
### 5. Create a cart DELETE endpoint to delete a item from the cart
Delete endpoint should also get item_id from the url
  
### 6. Create a User endpoint to get session id  
The user endpoint should take in first and last name from the body and return a session id (just a random string)

    session_id = secrets.token_urlsafe(TOKEN_SIZE)
  
### 7. Add session id as requirement in the header to cart enpoints to "secure" them
Check if session_id exists in the header:
    
    session_id = request.headers.get('Session-Id')
    
If not return a 401: Unauthorized

    Abort(401)

If there is a session id in the header but it does not exist in the list of session ids return a 403: Forbidden

    Abort(403)