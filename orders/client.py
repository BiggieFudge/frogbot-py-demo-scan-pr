"""Thin HTTP client for the downstream catalog service, backed by requests."""

import requests

from orders.config import load_config


class CatalogClient(object):
    def __init__(self, config=None):
        self.config = config or load_config()
        self.session = requests.Session()

    def _url(self, path):
        return "{base}/{path}".format(
            base=self.config["catalog_url"].rstrip("/"), path=path.lstrip("/")
        )

    def get_item(self, sku):
        response = self.session.get(
            self._url("/items/{0}".format(sku)),
            timeout=self.config["timeout_seconds"],
        )
        response.raise_for_status()
        return response.json()

    def reserve_item(self, sku, quantity):
        response = self.session.post(
            self._url("/items/{0}/reservations".format(sku)),
            json={"quantity": quantity},
            timeout=self.config["timeout_seconds"],
        )
        response.raise_for_status()
        return response.json()
