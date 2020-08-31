# Changelog

## 0.7.0

- A bit of cleanup, and start of some tests

## 0.6.0

- Improve parsing of write queries to handle more types and multiple queries per statement https://github.com/streeter/django-db-readonly/pull/17

## 0.5.0

- Add support for Django 1.10 and 1.11 by using the new style middleware https://github.com/streeter/django-db-readonly/pull/16

## 0.4.2

- Look up the `_last_executed` property on the underlying DB cursor https://github.com/streeter/django-db-readonly/pull/13

## 0.4.1

- Django 1.9 support https://github.com/streeter/django-db-readonly/pull/11

# v0.4

- Added per-Database configurability. https://github.com/streeter/django-db-readonly/pull/10

## 0.3.3

- Django 1.7+ support https://github.com/streeter/django-db-readonly/pull/8

## 0.3.2

- Fix [`_last_executed` exception](https://github.com/streeter/django-db-readonly/pull/3)

## 0.3.1

- ....

## 0.3.0

- Add `readonly` context processor

## 0.2.0

- Add exception catching middleware

## 0.1.1

- Minor optimizations
- PEP 8 cleanup

## 0.1.0

- Initial implementation
