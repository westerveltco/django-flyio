from __future__ import annotations

import os
from typing import Any
from warnings import warn

import dj_database_url


def get_db_config() -> dict[str, Any]:
    primary_region = os.getenv("PRIMARY_REGION", None)
    fly_region = os.getenv("FLY_REGION", None)
    database_url = os.getenv("DATABASE_URL", None)

    if not database_url:
        warn(
            "Environment variable `DATABASE_URL` is not set, using in-memory SQLite database",
            stacklevel=2,
        )
        return {"default": dj_database_url.parse("sqlite://:memory:")}

    if primary_region == fly_region:
        return {
            "default": dj_database_url.parse(database_url),
        }

    return {
        "default": dj_database_url.parse(database_url),
        "replica": dj_database_url.parse(database_url.replace(":5432/", ":5433/")),
    }
