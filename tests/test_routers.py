from __future__ import annotations

import os

from django_flyio.db import get_db_config
from django_flyio.routers import FlyDBReplicaRouter


def test_same_region(settings):
    os.environ["PRIMARY_REGION"] = "iad"
    os.environ["FLY_REGION"] = "iad"
    settings.DATABASES = get_db_config()

    router = FlyDBReplicaRouter()

    assert router.db_for_read(None) == "default"
    assert router.db_for_write(None) == "default"


def test_different_region(settings):
    os.environ["PRIMARY_REGION"] = "iad"
    os.environ["FLY_REGION"] = "lhr"
    settings.DATABASES = get_db_config()

    router = FlyDBReplicaRouter()

    assert router.db_for_read(None) == "replica"
    assert router.db_for_write(None) == "default"
