"""
Django DB Readonly
~~~~~~~~~~~~~~~~~~
"""
VERSION = (0, 4, 2)
__version__ = VERSION

from time import time

import django
from django.conf import settings
if django.VERSION < (1, 7):
    from django.db.backends import util
else:
    from django.db.backends import utils as util
from logging import getLogger

from readonly.exceptions import DatabaseWriteDenied


logger = getLogger('django.db.backends')


def _readonly():
    return getattr(settings, 'SITE_READ_ONLY', False)


def _get_readonly_dbs():
    read_on_db_names = []
    for db_key in getattr(settings, 'DB_READ_ONLY_DATABASES', tuple()):
        db = settings.DATABASES.get(db_key)
        if db:
            read_on_db_names.append(db['NAME'])
    return read_on_db_names


class ReadOnlyCursorWrapper(object):
    """
    This is a wrapper for a database cursor.

    This sits between django's own wrapper at
    `django.db.backends.util.CursorWrapper` and the database specific cursor at
    `django.db.backends.*.base.*CursorWrapper`. It overrides two specific
    methods: `execute` and `executemany`. If the site is in read-only mode,
    then the SQL is examined to see if it contains any write actions. If a
    write is detected, an exception is raised.

    A site is in read only mode by setting the SITE_READ_ONLY setting. For
    obvious reasons, this is False by default.

    Raises a DatabaseWriteDenied exception if writes are disabled.
    """

    SQL_WRITE_BLACKLIST = (
        # Data Definition
        'CREATE', 'ALTER', 'RENAME', 'DROP', 'TRUNCATE',
        # Data Manipulation
        'INSERT INTO', 'UPDATE', 'REPLACE', 'DELETE FROM',
    )

    def __init__(self, cursor, db):
        self.cursor = cursor
        self.db = db
        self.readonly = _readonly()
        self.readonly_dbs = _get_readonly_dbs()

    def execute(self, sql, params=()):
        # Check the SQL
        if (self.readonly
                and self._write_sql(sql)
                and self._write_to_readonly_db()):
            raise DatabaseWriteDenied
        return self.cursor.execute(sql, params)

    def executemany(self, sql, param_list):
        # Check the SQL
        if self.readonly and self._write_sql(sql):
            raise DatabaseWriteDenied
        return self.cursor.executemany(sql, param_list)

    def __getattr__(self, attr):
        return getattr(self.cursor, attr)

    def __iter__(self):
        return iter(self.cursor)

    def _write_sql(self, sql):
        return sql.startswith(self.SQL_WRITE_BLACKLIST)

    def _write_to_readonly_db(self):
        return (
            not self.readonly_dbs
            or self.db.settings_dict['NAME'] in self.readonly_dbs)

    @property
    def _last_executed(self):
        return getattr(self.cursor, '_last_executed', '')

class CursorWrapper(util.CursorWrapper):
    def __init__(self, cursor, db):
        self.cursor = ReadOnlyCursorWrapper(cursor, db)
        self.db = db


# Redefine CursorDebugWrapper because we want it to inherit from *our*
# CursorWrapper instead of django.db.backends.util.CursorWrapper
class CursorDebugWrapper(CursorWrapper):

    def execute(self, sql, params=()):
        start = time()
        try:
            return self.cursor.execute(sql, params)
        finally:
            stop = time()
            duration = stop - start
            sql = self.db.ops.last_executed_query(self.cursor, sql, params)
            self.db.queries.append({
                'sql': sql,
                'time': "%.3f" % duration,
            })
            logger.debug(
                '(%.3f) %s; args=%s',
                duration, sql, params,
                extra={'duration': duration, 'sql': sql, 'params': params}
            )

    def executemany(self, sql, param_list):
        start = time()
        try:
            return self.cursor.executemany(sql, param_list)
        finally:
            stop = time()
            duration = stop - start
            self.db.queries.append({
                'sql': '%s times: %s' % (len(param_list), sql),
                'time': "%.3f" % duration,
            })
            logger.debug(
                '(%.3f) %s; args=%s',
                duration, sql, param_list,
                extra={'duration': duration, 'sql': sql, 'params': param_list}
            )

if _readonly():
    # Monkey Patching!
    util.CursorWrapper = CursorWrapper
    util.CursorDebugWrapper = CursorDebugWrapper
