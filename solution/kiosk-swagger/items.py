ITEMS = [
    {'id': 0, 'name': 'apple'},
    {'id': 1, 'name': 'banana'},
    {'id': 2, 'name': 'orange'},
    {'id': 3, 'name': 'pineapple'},
]


def get(item_id):
    for item in ITEMS:
        if item['id'] == item_id:
            return item

    return None


def list():
    return ITEMS
