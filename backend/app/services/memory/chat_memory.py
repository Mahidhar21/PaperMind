chat_sessions = {}


def add_message(session_id, role, content):

    if session_id not in chat_sessions:
        chat_sessions[session_id] = []

    chat_sessions[session_id].append({
        "role": role,
        "content": content
    })


def get_chat_history(session_id):

    return chat_sessions.get(session_id, [])