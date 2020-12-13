import os

SQL_LITE_SETTINGS = {
    'provider': 'sqlite',
    'filename': 'sqlite.db',
    'create_db': True,
}

MYSQL_SETTINGS = {
    'user': os.getenv('MYSQL_USER'),
    'passwd': os.getenv('MYSQL_PASSWORD'),
    'host': os.getenv('MYSQL_HOST') or 'localhost',
    'port': os.getenv('MYSQL_PORT') or 3306,
    'db': 'AIBot',
    'provider': 'mysql',
}

DEFAULT_TOPIC = 'Tennis'

TOKEN = os.getenv('TOKEN')
