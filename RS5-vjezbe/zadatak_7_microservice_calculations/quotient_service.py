from aiohttp import web


async def kolicnik_handler(request: web.Request) -> web.Response:
    try:
        payload = await request.json()
    except Exception:
        return web.json_response({"error": "Ocekivan je JSON objekt."}, status=400)

    if not isinstance(payload, dict):
        return web.json_response({"error": "Ocekivan je JSON objekt."}, status=400)

    zbroj = payload.get("zbroj")
    umnozak = payload.get("umnozak")

    if zbroj is None or umnozak is None:
        return web.json_response(
            {"error": "Potrebni su kljucevi 'zbroj' i 'umnozak'."}, status=400
        )

    try:
        zbroj_value = float(zbroj)
        umnozak_value = float(umnozak)
    except (TypeError, ValueError):
        return web.json_response({"error": "Vrijednosti moraju biti brojevi."}, status=400)

    if zbroj_value == 0:
        return web.json_response(
            {"error": "Dijeljenje s 0 nije dozvoljeno."}, status=400
        )

    return web.json_response({"kolicnik": umnozak_value / zbroj_value})


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_post("/kolicnik", kolicnik_handler)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), port=8085)
