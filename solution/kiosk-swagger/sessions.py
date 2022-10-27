import re
import secrets

TOKEN_SIZE = 16  # bytes
SESSIONS = {}


def create(first, last):
    if _is_invalid_name(first):
        raise Exception('Invalid first name.')

    if _is_invalid_name(last):
        raise Exception('Invalid last name.')

    session_id = secrets.token_urlsafe(TOKEN_SIZE)

    SESSIONS[session_id] = {
        'first_name': first,
        'last_name': last,
    }

    return session_id


def is_valid(session_id):
    return session_id in SESSIONS


def _is_invalid_name(name):
    # Name shall not be empty, or contain invalid characters.
    return name is None or len(name) < 1 or re.search('[^a-zA-Z0-9\\- ]', name) is not None
