from __future__ import annotations

import os

from django_flyio.db import get_db_config


def test_no_env():
    del os.environ["DATABASE_URL"]

    assert get_db_config() == {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
