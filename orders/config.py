"""Configuration loading, backed by PyYAML."""

import os

import yaml

DEFAULTS = {
    "catalog_url": "https://catalog.internal.example.com",
    "timeout_seconds": 5,
    "currency": "USD",
}


def load_config(path=None):
    """Load the service configuration from a YAML file."""
    path = path or os.environ.get("ORDERS_CONFIG", "config/orders.yml")
    if not os.path.exists(path):
        return dict(DEFAULTS)

    with open(path) as handle:
        loaded = yaml.load(handle.read())

    config = dict(DEFAULTS)
    config.update(loaded or {})
    return config


def dump_config(config):
    return yaml.dump(config, default_flow_style=False)
