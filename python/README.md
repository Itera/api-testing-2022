# Simple Flask app with Swagger UI

Some description here.

## Prerequisites

It is assumed Python 3.x is available.

## Run in unix (-like) shell

Initiate virtual environment and install required dependencies with:

```
./init.sh
```

Activate the virtual environment and enable Flask dev-mode:

```
source ./venv/Scripts/activate
FLASK_ENV=development
```

Finally, run your Python application with Flask:

```
flask run
```

## Run in CMD

Initiate virtual environment and install required dependencies with:

```
.\init.bat
```

Activate the virtual environment and enable Flask dev-mode:

```
.\venv\Scripts\activate.bat
SET FLASK_ENV=development
```

Finally, run your Python application with Flask:

```
flask run
```

## Swagger UI

Swagger UI should now be available at http://localhost:5000 .
