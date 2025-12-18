import asyncio
from aiohttp import ClientSession, web

CATFACT_SINGLE_URL = "https://catfact.ninja/fact"
DEFAULT_AMOUNT = 5


async def fetch_fact(session: ClientSession) -> str:
    async with session.get(CATFACT_SINGLE_URL) as response:
        response.raise_for_status()
        payload = await response.json()
        return payload.get("fact", "")


async def fetch_facts(amount: int) -> list[str]:
    async with ClientSession() as session:
        tasks = [asyncio.create_task(fetch_fact(session)) for _ in range(amount)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    facts: list[str] = []
    for result in results:
        if isinstance(result, Exception):
            continue
        if isinstance(result, str):
            facts.append(result)
    return facts


async def cats_handler(request: web.Request) -> web.Response:
    facts = await fetch_facts(DEFAULT_AMOUNT)
    return web.json_response({"facts": facts})


async def cat_amount_handler(request: web.Request) -> web.Response:
    try:
        amount = int(request.match_info["amount"])
    except (KeyError, ValueError):
        return web.json_response({"error": "Amount mora biti cijeli broj."}, status=400)

    if amount <= 0:
        return web.json_response(
            {"error": "Amount mora biti pozitivan cijeli broj."}, status=400
        )

    facts = await fetch_facts(amount)
    return web.json_response({"facts": facts, "amount": amount})


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/cats", cats_handler)
    app.router.add_get("/cat/{amount}", cat_amount_handler)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), port=8086)
