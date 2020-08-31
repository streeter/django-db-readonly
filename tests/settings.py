SECRET_KEY = "notsecr3t"

DB_READ_ONLY_MIDDLEWARE_MESSAGE = False
SITE_READ_ONLY = False
DB_READ_ONLY_DATABASES = False

DATABASE_ENGINE = "sqlite3"

# Uncomment below to run tests with mysql
# DATABASE_ENGINE = "django.db.backends.mysql"
# DATABASE_NAME = "readonly_test"
# DATABASE_USER = "readonly_test"
# DATABASE_HOST = "/var/mysql/mysql.sock"

INSTALLED_APPS = [
    "readonly",
]

MIDDLEWARE = [
    "readonly.middleware.DatabaseReadOnlyMiddleware",
]
