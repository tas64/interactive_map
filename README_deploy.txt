Чтобы запустить сервер, необходимо сделать создать файл с локальными настройками, для БД.

Файл должен находиться здесь: src/server/local_settings.py

он должен иметь следующее содержание:

OUR_DATABASE_HOST = 'localhost'
OUR_DATABASE_NAME = 'test_db'
OUR_DATABASE_USER = 'test_user'
OUR_DATABASE_PASSWORD = 'test_pass'


#for django ORM
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': OUR_DATABASE_NAME,                      # Or path to database file if using sqlite3.
        'USER': OUR_DATABASE_USER,                      # Not used with sqlite3.
        'PASSWORD': OUR_DATABASE_PASSWORD,                  # Not used with sqlite3.
        'HOST': OUR_DATABASE_HOST,                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
