from __future__ import annotations

import os
import uuid

import pytest


@pytest.fixture(
    params=[
        "iad",
        "lhr",
    ],
)
def fly_server(request):
    allocation_id = uuid.uuid4().hex.rsplit("-", maxsplit=1)[-1]
    region = request.param
    os.environ["FLY_ALLOC_ID"] = allocation_id
    os.environ["FLY_REGION"] = region
    return {"allocation_id": allocation_id, "region": region}


def test_sync(client, fly_server):
    response = client.get("/")
    assert response.headers["Fly-Server"] == f"{fly_server['allocation_id']}-{fly_server['region']}"


@pytest.mark.asyncio
async def test_async(async_client, fly_server):
    response = await async_client.get("/async/")
    assert response.headers["Fly-Server"] == f"{fly_server['allocation_id']}-{fly_server['region']}"


def test_no_env(client):
    del os.environ["FLY_ALLOC_ID"]
    del os.environ["FLY_REGION"]

    response = client.get("/")
    assert response.headers["Fly-Server"] == "unknown"
