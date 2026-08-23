"""HTTP handlers for the orders service."""

import json

from django.http import HttpResponse, JsonResponse

from orders.client import CatalogClient
from orders.config import dump_config, load_config

_client = None


def _catalog():
    global _client
    if _client is None:
        _client = CatalogClient()
    return _client


def health(request):
    return JsonResponse({"status": "ok"})


def config(request):
    return HttpResponse(dump_config(load_config()), content_type="text/yaml")


def item(request, sku):
    return JsonResponse(_catalog().get_item(sku))


def reserve(request, sku):
    payload = json.loads(request.body.decode("utf-8") or "{}")
    quantity = int(payload.get("quantity", 1))
    return JsonResponse(_catalog().reserve_item(sku, quantity))
