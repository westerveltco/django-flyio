from __future__ import annotations

from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def index(request):  # noqa: ARG001
    return HttpResponse("Index")


async def async_(request):  # noqa: ARG001
    return HttpResponse("Asynchronous")
