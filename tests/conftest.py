from __future__ import annotations

import os
import uuid

import pytest

from django_flyio.db import get_db_config


@pytest.fixture(autouse=True)
def database_url():
    os.environ["DATABASE_URL"] = "postgres://postgres@localhost:5432/postgres"
