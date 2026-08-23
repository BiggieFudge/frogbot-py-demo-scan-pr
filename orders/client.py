"""HTTP client for the downstream catalog service, backed by urllib3."""

import json

import urllib3

from orders.config import load_config


class CatalogClient(object):
    def __init__(self, config=None):
        self.config = config or load_config()
        self.pool = urllib3.PoolManager(retries=urllib3.Retry(total=2))

    def _url(self, path):
        return "{base}/{path}".format(
            base=self.config["catalog_url"].rstrip("/"), path=path.lstrip("/")
        )

    def _request(self, method, path, body=None):
        headers = {"Accept": "application/json"}
        encoded = None
        if body is not None:
            headers["Content-Type"] = "application/json"
            encoded = json.dumps(body).encode("utf-8")

        response = self.pool.request(
            method,
            self._url(path),
            body=encoded,
            headers=headers,
            timeout=urllib3.Timeout(total=self.config["timeout_seconds"]),
        )
        if response.status >= 400:
            raise RuntimeError(
                "catalog returned {0} for {1}".format(response.status, path)
            )
        return json.loads(response.data.decode("utf-8"))

    def get_item(self, sku):
        return self._request("GET", "/items/{0}".format(sku))

    def reserve_item(self, sku, quantity):
        return self._request(
            "POST",
            "/items/{0}/reservations".format(sku),
            body={"quantity": quantity},
        )
