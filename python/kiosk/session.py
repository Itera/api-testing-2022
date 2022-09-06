import secrets


TOKEN_SIZE = 16  # bytes
SESSIONS = {}


def create_session(first, last):
    session_id = secrets.token_urlsafe(TOKEN_SIZE)

    SESSIONS[session_id] = {
        'first_name': first,
        'last_name': last,
    }

    return session_id


def check_session_id(session_id):
    return session_id in SESSIONS
