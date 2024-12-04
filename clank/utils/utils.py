import uuid


def create_session_id():
    """
    create an ID to identify different sessions (conversations?)
    """
    return str(uuid.uuid4())