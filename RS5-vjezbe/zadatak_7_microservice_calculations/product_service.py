from aiohttp import web
import math


async def umnozak_handler(request: web.Request) -> web.Response:
    try:
        numbers = await request.json()
    except Exception:
        return web.json_response({"error": "Tijelo mora biti lista brojeva."}, status=400)

    if not isinstance(numbers, list) or not numbers:
        return web.json_response({"error": "Tijelo mora biti ne-prazna lista brojeva."}, status=400)

    try:
        product = math.prod(float(num) for num in numbers)
    except (TypeError, ValueError):
        return web.json_response({"error": "Svi elementi moraju biti brojevi."}, status=400)

    return web.json_response({"umnozak": product})


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_post("/umnozak", umnozak_handler)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), port=8084)
