from django.db.utils import DatabaseError


class DatabaseWriteDenied(DatabaseError):
    pass
