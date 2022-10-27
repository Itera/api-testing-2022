from flask import Flask, jsonify

app = Flask(__name__)

ITEMS = [
    'apple',
    'banana',
    'pineapple',
]


@app.get('/kiosk/items')
def get_items():
    return jsonify(ITEMS)


app.run()
