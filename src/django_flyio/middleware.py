# Portions of this file are derived from django-cors-headers:
# https://github.com/adamchainz/django-cors-headers
# django-cors-headers is licensed under the MIT License and is
# Copyright (c) 2017 Otto Yiu (https://ottoyiu.com) and other
# contributors.

from __future__ import annotations

import asyncio
import os
from http import HTTPStatus
from typing import Awaitable
from typing import Callable

from django.http import HttpRequest
from django.http.response import HttpResponse
from django.http.response import HttpResponseBase

try:
    from psycopg.errors import ReadOnlySqlTransaction
except ImportError:
    from psycopg2.errors import ReadOnlySqlTransaction

FLY_SERVER = "fly-server"
FLY_REPLAY = "fly-replay"


class FlyResponseMiddleware:
    sync_capable = True
    async_capable = True

    def __init__(
        self,
        get_response: (
            Callable[[HttpRequest], HttpResponseBase]
            | Callable[[HttpRequest], Awaitable[HttpResponseBase]]
        ),
    ) -> None:
        self.get_response = get_response
        if asyncio.iscoroutinefunction(self.get_response):
            # Mark the class as async-capable, but do the actual switch
            # inside __call__ to avoid swapping out dunder methods
            self._is_coroutine = asyncio.coroutines._is_coroutine  # type: ignore [attr-defined]
        else:
            self._is_coroutine = None

    def __call__(
        self, request: HttpRequest
    ) -> HttpResponseBase | Awaitable[HttpResponseBase]:
        if self._is_coroutine:
            return self.__acall__(request)
        response = self.get_response(request)
        assert isinstance(response, HttpResponseBase)  # noqa: S101
        self.add_response_headers(response)
        return response

    async def __acall__(self, request: HttpRequest) -> HttpResponseBase:
        aresponse = self.get_response(request)
        assert not isinstance(aresponse, HttpResponseBase)  # noqa: S101
        response = await aresponse
        self.add_response_headers(response)
        return response

    def add_response_headers(self, response: HttpResponseBase) -> None:
        if FLY_SERVER not in response:
            machine_id = os.getenv("FLY_ALLOC_ID", None)
            region = os.getenv("FLY_REGION", None)
            if machine_id and region:
                response[FLY_SERVER] = f"{machine_id}-{region}"
            else:
                response[FLY_SERVER] = "unknown"


class FlyReplayMiddleware:
    sync_capable = True
    async_capable = True

    def __init__(
        self,
        get_response: (
            Callable[[HttpRequest], HttpResponseBase]
            | Callable[[HttpRequest], Awaitable[HttpResponseBase]]
        ),
    ) -> None:
        self.get_response = get_response
        if asyncio.iscoroutinefunction(self.get_response):
            # Mark the class as async-capable, but do the actual switch
            # inside __call__ to avoid swapping out dunder methods
            self._is_coroutine = asyncio.coroutines._is_coroutine  # type: ignore [attr-defined]
        else:
            self._is_coroutine = None

    def __call__(
        self, request: HttpRequest
    ) -> HttpResponseBase | Awaitable[HttpResponseBase]:
        return (
            self.__acall__(request)
            if self._is_coroutine
            else self.get_response(request)
        )

    async def __acall__(self, request: HttpRequest) -> HttpResponseBase:
        aresponse = self.get_response(request)
        assert not isinstance(aresponse, HttpResponseBase)  # noqa: S101
        return await aresponse

    def process_exception(
        self, request: HttpRequest, exception: Exception
    ) -> HttpResponseBase:  # noqa: ARG002
        if isinstance(exception, ReadOnlySqlTransaction):
            primary_region = os.getenv("PRIMARY_REGION", None)
            response = HttpResponse()
            response.content = response.make_bytes(f"retry in region {primary_region}")
            response.status_code = HTTPStatus.CONFLICT
            response[FLY_REPLAY] = f"region={primary_region}"
            return response
