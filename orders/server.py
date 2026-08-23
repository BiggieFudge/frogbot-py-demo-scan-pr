"""HTTP surface of the orders service, backed by aiohttp."""

from aiohttp import web

from orders.client import CatalogClient
from orders.config import load_config
from orders.tokens import sign_receipt


async def health(request):
    return web.json_response({"status": "ok"})


async def get_item(request):
    client = request.app["catalog"]
    sku = request.match_info["sku"]
    return web.json_response(client.get_item(sku))


async def reserve_item(request):
    client = request.app["catalog"]
    sku = request.match_info["sku"]
    payload = await request.json()
    quantity = int(payload.get("quantity", 1))

    reservation = client.reserve_item(sku, quantity)
    receipt = {"sku": sku, "quantity": quantity, "reservation": reservation}
    return web.json_response(
        {"receipt": receipt, "signature": sign_receipt(receipt)}
    )


def create_app(config=None):
    config = config or load_config()
    app = web.Application()
    app["config"] = config
    app["catalog"] = CatalogClient(config)
    app.add_routes(
        [
            web.get("/health", health),
            web.get("/items/{sku}", get_item),
            web.post("/items/{sku}/reservations", reserve_item),
        ]
    )
    return app


def main():
    config = load_config()
    web.run_app(create_app(config), port=config["listen_port"])


if __name__ == "__main__":
    main()
