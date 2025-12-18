import asyncio
from aiohttp import web


async def pozdrav_handler(request: web.Request) -> web.Response:
    await asyncio.sleep(4)
    return web.json_response({"message": "Pozdrav nakon 4 sekunde"})


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/pozdrav", pozdrav_handler)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), port=8082)
