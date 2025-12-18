import asyncio
from aiohttp import ClientSession, web
from typing import Any, List, Dict

PROIZVODI: List[Dict[str, Any]] = [
    {"id": 1, "naziv": "Laptop", "cijena": 5000},
    {"id": 2, "naziv": "Mis", "cijena": 100},
    {"id": 3, "naziv": "Tipkovnica", "cijena": 200},
    {"id": 4, "naziv": "Monitor", "cijena": 1000},
    {"id": 5, "naziv": "Slusalice", "cijena": 50},
]

narudzbe: List[Dict[str, Any]] = []


async def get_products_handler(request: web.Request) -> web.Response:
    return web.json_response(PROIZVODI)


async def get_product_by_id_handler(request: web.Request) -> web.Response:
    proizvod_id = int(request.match_info["id"])
    for proizvod in PROIZVODI:
        if proizvod["id"] == proizvod_id:
            return web.json_response(proizvod)
    return web.json_response(
        {"error": "Proizvod s trazenim ID-em ne postoji"}, status=404
    )


async def post_order_handler(request: web.Request) -> web.Response:
    payload = await request.json()
    proizvod_id = payload.get("proizvod_id")
    kolicina = payload.get("kolicina")

    for proizvod in PROIZVODI:
        if proizvod["id"] == proizvod_id:
            narudzba = {
                "proizvod_id": proizvod_id,
                "kolicina": kolicina,
                "naziv": proizvod["naziv"],
            }
            narudzbe.append(narudzba)
            return web.json_response(narudzbe, status=201)

    return web.json_response(
        {"error": "Proizvod s trazenim ID-em ne postoji"}, status=404
    )


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/proizvodi", get_products_handler)
    app.router.add_get("/proizvodi/{id}", get_product_by_id_handler)
    app.router.add_post("/narudzbe", post_order_handler)
    return app


async def run_client_tests(base_url: str) -> None:
    async with ClientSession() as session:
        async with session.get(f"{base_url}/proizvodi") as resp:
            print("GET /proizvodi ->", resp.status, await resp.json())

        async with session.get(f"{base_url}/proizvodi/2") as resp:
            print("GET /proizvodi/2 ->", resp.status, await resp.json())

        async with session.get(f"{base_url}/proizvodi/42") as resp:
            print("GET /proizvodi/42 ->", resp.status, await resp.json())

        async with session.post(
            f"{base_url}/narudzbe", json={"proizvod_id": 3, "kolicina": 2}
        ) as resp:
            print("POST /narudzbe (valid) ->", resp.status, await resp.json())

        async with session.post(
            f"{base_url}/narudzbe", json={"proizvod_id": 99, "kolicina": 1}
        ) as resp:
            print("POST /narudzbe (missing product) ->", resp.status, await resp.json())


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
