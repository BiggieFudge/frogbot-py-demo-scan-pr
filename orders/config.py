"""Configuration loading for the orders service."""

import json
import os

DEFAULTS = {
    "catalog_url": "https://catalog.internal.example.com",
    "timeout_seconds": 5,
    "currency": "USD",
    "listen_port": 8080,
}


def load_config(path=None):
    """Load the service configuration, falling back to the built-in defaults."""
    path = path or os.environ.get("ORDERS_CONFIG", "config/orders.json")
    config = dict(DEFAULTS)

    if os.path.exists(path):
        with open(path) as handle:
            config.update(json.load(handle) or {})

    if "ORDERS_CATALOG_URL" in os.environ:
        config["catalog_url"] = os.environ["ORDERS_CATALOG_URL"]

    return config
