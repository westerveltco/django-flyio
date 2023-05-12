from __future__ import annotations

import os

import pytest


@pytest.fixture(autouse=True)
def database_url():
    os.environ["DATABASE_URL"] = "postgres://postgres@localhost:5432/postgres"
