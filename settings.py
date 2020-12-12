import os

SQL_LITE_SETTINGS = {
    'provider': 'sqlite',
    'filename': 'sqlite.db',
    'create_db': True,
}

DEFAULT_TOPIC = 'Tennis'

TOKEN = os.getenv('TOKEN')
