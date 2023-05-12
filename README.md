# django-flyio

[![PyPI - Version](https://img.shields.io/pypi/v/django-flyio.svg)](https://pypi.org/project/django-flyio)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-flyio.svg)](https://pypi.org/project/django-flyio)

---

A set of simple utilities for Django apps running on [Fly.io](https://fly.io).

**Note:** This package is designed to work with [V2 Apps](https://fly.io/docs/reference/apps/). It has not been tested with V1 Apps.

## Installation

```shell
pip install django-flyio
```

## Usage

### Multi-Region Fly Postgres

1.  Set your `DATABASES` settings to call `get_db_config` from `django_flyio.db`.

    This function reads the `PRIMARY_REGION` and `FLY_REGION` environment variables to determine the Fly region the primary database is in and the Fly region the app is currently running in.

2.  Add `django_flyio.routers.FlyDBReplicaRouter` to your `DATABASE_ROUTERS` settings.

    This router reads whether the `DATABASES` setting has a `replica` key and, if so, routes reads to the replica database.

```python
# settings.py
from django_flyio.db import get_db_config
from django_flyio.routers import FlyDBReplicaRouter

DATABASES = get_db_config()

DATABASE_ROUTERS = [FlyDBReplicaRouter]
```

### Middleware

To set the `Fly-Server` header containing the Fly server and region that served the request, add `django_flyio.middleware.FlyResponseMiddleware` to your `MIDDLEWARE` settings.

```python
# settings.py
MIDDLEWARE = [
    # ...
    'django_flyio.middleware.FlyResponseMiddleware',
]
```

## License

`django-flyio` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
