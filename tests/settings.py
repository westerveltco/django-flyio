from __future__ import annotations

from django_flyio.routers import FlyDBReplicaRouter

SECRET_KEY = "NOTASECRET"

ALLOWED_HOSTS = ["*"]

DATABASE_ROUTERS = [FlyDBReplicaRouter]

ROOT_URLCONF = "tests.urls"

MIDDLEWARE = ["django_flyio.middleware.FlyResponseMiddleware"]

USE_TZ = True
