## About

An way to globally disable writes to your database. This works by
inserting a cursor wrapper between Django's `CursorWrapper` and
the database connection's cursor wrapper. So many cursor wrappers!


## Installation

I uploaded it to [PyPi][pypi], so you can grab it there if you'd like with

```bash
pip install django-db-readonly
```

or install with pip the git address:

```bash
pip install git+git@github.com:streeter/django-db-readonly.git
```

You're choice. Then add `readonly` to your `INSTALLED_APPS`.

```python
INSTALLED_APPS = (
    # ...
    'readonly',
    # ...
)
```


## Usage

You shouldn't notice this at all, _unless_ you add the following line
to your `settings.py`:

```python
# Set to False to allow writes
SITE_READ_ONLY = True
```

When you do this, any write action to your databases will generate an
exception. You should catch this exception and deal with it somehow. Or
let Django display an [error 500 page][error500]. The exception you will
want to catch is `readonly.exceptions.DatabaseWriteDenied` which inherits
from `django.db.utils.DatabaseError`.

There is also a middleware class that will handle the exceptions and attempt
to handle them smartly. Add the following line in your `settings.py`:

```python
MIDDLEWARE_CLASSES = (
    # ...
    'readonly.middleware.DatabaseReadOnlyMiddleware',
    # ...
)
```

This will then enable the middleware which will catch `DatabaseWriteDenied`
exceptions. If the request is a POST request, we will redirect the user to the
same URL, but as a GET request. If the request is not a POST (ie. a GET), we
will just display a `HttpResponse` with text telling the user the site
is in read-only mode.

In addition, the middleware class can add an error-type message using the
`django.contrib.messages` module. Add:

```python
# Enable
DB_READ_ONLY_MIDDLEWARE_MESSAGE = True
```

to your `settings.py` and then on POST requests that generate a
`DatabaseWriteDenied` exception, we will add an error message informing the
user that the site is in read-only mode.

For additional messaging, there is a context processor that adds
`SITE_READ_ONLY` into the context. Add the following line in your `settings.py`:

```python
TEMPLATE_CONTEXT_PROCESSORS = (
    # ...
    'readonly.context_processors.readonly',
    # ...
)
```

And use it as you would any boolean in the template, e.g. `{% if SITE_READ_ONLY
%} We're down for maintenance. {% endif %}`

## Testing

There aren't any tests included, yet. Run it at your own peril.


## Caveats

This will work with [Django Debug Toolbar][ddt]. In fact, I was inspired
by [DDT's sql panel][sql-panel] when writing this app.

However, in order for both DDT _and_ django-db-readonly to work, you need
to make sure that you have `readonly` before `debug_toolbar` in your
`INSTALLED_APPS`. Otherwise, you are responsible for debugging what is
going on. Of course, I'm not sure why you'd be running DDT in production
and running django-db-readonly in development, but whatever, I'm not you.

More generally, if you have any other apps that modifies either
`django.db.backends.util.CursorWrapper` or
`django.db.backends.util.CursorDebugWrapper`, you need to make sure
that `readonly` is placed _before_ of those apps in `INSTALLED_APPS`.


## The Nitty Gritty

How does this do what it does? Well, django-db-readonly sits between
Django's own cursor wrapper at `django.db.backends.util.CursorWrapper` and
the database specific cursor at `django.db.backends.*.base.*CursorWrapper`.
It overrides two specific methods: `execute` and `executemany`. If the
site is in read-only mode, then the SQL is examined to see if it
contains any write actions (defined in
`readonly.ReadOnlyCursorWrapper.SQL_WRITE_BLACKLIST`). If a write is
detected, an exception is raised.


[pypi]: http://pypi.python.org/pypi/django-db-readonly/
[error500]: http://docs.djangoproject.com/en/1.3/topics/http/urls/#handler500
[ddt]: https://github.com/robhudson/django-debug-toolbar
[sql-panel]: https://github.com/robhudson/django-debug-toolbar/blob/master/debug_toolbar/panels/sql.py
