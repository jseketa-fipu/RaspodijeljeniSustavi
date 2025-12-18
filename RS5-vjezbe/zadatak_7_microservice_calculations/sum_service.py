from aiohttp import web


async def zbroj_handler(request: web.Request) -> web.Response:
    try:
        numbers = await request.json()
    except Exception:
        return web.json_response({"error": "Tijelo mora biti lista brojeva."}, status=400)

    if not isinstance(numbers, list) or not numbers:
        return web.json_response({"error": "Tijelo mora biti ne-prazna lista brojeva."}, status=400)

    try:
        total = sum(float(num) for num in numbers)
    except (TypeError, ValueError):
        return web.json_response({"error": "Svi elementi moraju biti brojevi."}, status=400)

    return web.json_response({"zbroj": total})


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_post("/zbroj", zbroj_handler)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), port=8083)
