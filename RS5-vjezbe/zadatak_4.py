import asyncio
from aiohttp import ClientSession, web
from typing import Any, List, Dict

PROIZVODI: List[Dict[str, Any]] = [
    {"id": 1, "naziv": "Laptop", "cijena": 5000.0, "kolicina": 2},
    {"id": 2, "naziv": "Miš", "cijena": 100.0, "kolicina": 15},
    {"id": 3, "naziv": "Tipkovnica", "cijena": 200.0, "kolicina": 12},
    {"id": 4, "naziv": "Monitor", "cijena": 1000.0, "kolicina": 7},
    {"id": 5, "naziv": "Slušalice", "cijena": 50.0, "kolicina": 100},
]


async def get_proizvodi(request: web.Request) -> web.Response:
    return web.json_response(PROIZVODI)


async def get_proizvod_po_id(request: web.Request) -> web.Response:
    proizvod_id = int(request.match_info["id"])
    for proizvod in PROIZVODI:
        if proizvod["id"] == proizvod_id:
            return web.json_response(proizvod)
    return web.json_response(
        {"error": "Proizvod s traženim ID-em ne postoji"}, status=404
    )


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/proizvodi", get_proizvodi)
    app.router.add_get("/proizvodi/{id}", get_proizvod_po_id)
    return app


async def run_client_tests(base_url: str) -> None:
    async with ClientSession() as session:
        async with session.get(f"{base_url}/proizvodi") as resp:
            print("GET /proizvodi ->", resp.status, await resp.json())

        async with session.get(f"{base_url}/proizvodi/3") as resp:
            print("GET /proizvodi/3 ->", resp.status, await resp.json())

        async with session.get(f"{base_url}/proizvodi/999") as resp:
            print("GET /proizvodi/999 ->", resp.status, await resp.json())


async def main() -> None:
    app = create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, port=8081)
    await site.start()
    try:
        await run_client_tests("http://localhost:8081")
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
