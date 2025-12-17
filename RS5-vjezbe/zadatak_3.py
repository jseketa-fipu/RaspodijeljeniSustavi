from aiohttp import web
from typing import Any, List, Dict

korisnici: List[Dict[str, Any]] = [
    {"ime": "Ivo", "godine": 25},
    {"ime": "Ana", "godine": 17},
    {"ime": "Marko", "godine": 19},
    {"ime": "Maja", "godine": 16},
    {"ime": "Iva", "godine": 22},
]


async def punoljetni_handler(request: web.Request) -> web.Response:
    punoljetni = [korisnik for korisnik in korisnici if korisnik["godine"] >= 18]
    return web.json_response(punoljetni)


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/punoljetni", punoljetni_handler)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), port=8082)
