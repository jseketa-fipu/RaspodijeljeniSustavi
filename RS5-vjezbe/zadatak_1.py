from aiohttp import web

# Hard-coded set of products that the service returns.
PROIZVODI: list[dict[str, int | str]] = [
    {"id": 1, "naziv": "Laptop", "cijena": 5000},
    {"id": 2, "naziv": "Miš", "cijena": 100},
    {"id": 3, "naziv": "Tipkovnica", "cijena": 200},
    {"id": 4, "naziv": "Monitor", "cijena": 1000},
    {"id": 5, "naziv": "Slušalice", "cijena": 50},
]


async def get_products_handler(request: web.Request) -> web.Response:
    """Return the list of products as JSON."""
    return web.json_response(PROIZVODI)


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/proizvodi", get_products_handler)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), port=8081)
