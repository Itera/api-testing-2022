ITEMS = [
    {'id': 0, 'name': 'banana'},
    {'id': 1, 'name': 'pineapple'},
    {'id': 2, 'name': 'apple'},
    {'id': 3, 'name': 'pen'},
]


def get_item(item_id):
    for item in ITEMS:
        if item['id'] == item_id:
            return item

    raise Exception('Item not found.')


def list_items():
    return ITEMS
