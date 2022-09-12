# Simple Flask app

Some description here.

## Prerequisites

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

## Run the service

Flask has a "development mode", which will automatically reload your service
whenever the source changes. To enable, you'll need to set and environment
variable.

On Unix-like systems:

```
FLASK_ENV=development
```

or on the Windows Command Line:

```
SET FLASK_ENV=development
```

Now run Flask from the app folder, it will automatically load `app.py` if
available:

```
flask run
```

If this doesn't work properly for some reason, you may want to try to run it
with Python:

```
python -m flask run
```

## Swagger UI

For the `kiosk_swagger` app, Swagger UI should now be available at
http://localhost:5000 .
