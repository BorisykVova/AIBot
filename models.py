from pony import orm

from settings import MYSQL_SETTINGS, DEFAULT_TOPIC


db = orm.Database(**MYSQL_SETTINGS)


class User(db.Entity):
    id = orm.PrimaryKey(int)
    current_topic = orm.Required(str, default=DEFAULT_TOPIC)


db.generate_mapping(create_tables=True)
