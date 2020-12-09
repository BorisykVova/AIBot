from pony import orm

import logger
from models import User
from settings import DEFAULT_TOPIC

log = logger.get_logger('User CRUD')

@orm.db_session
def get(user_id: int) -> User:
    user = User[user_id]
    return user


@orm.db_session
def create(user_id: int, topic: str = DEFAULT_TOPIC) -> User:
    user = User(id=user_id, current_topic=topic)
    log.debug(f'User[{user.id}] was created.')
    return user


@orm.db_session
def get_or_create(user_id: int, topic: str = DEFAULT_TOPIC) -> User:
    try:
        return get(user_id)
    except orm.ObjectNotFound:
        return create(user_id, topic)


@orm.db_session
def update(user_id: int, topic: str) -> User:
    user = get(user_id)
    user.current_topic = topic
    return user
