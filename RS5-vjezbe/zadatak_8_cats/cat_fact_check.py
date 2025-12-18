from aiohttp import web


def contains_cat_word(fact: str) -> bool:
    return "cat" in fact.lower()


async def facts_handler(request: web.Request) -> web.Response:
    try:
        payload = await request.json()
    except Exception:
        return web.json_response({"error": "Ocekivan je JSON objekt."}, status=400)

    facts = payload.get("facts")
    if not isinstance(facts, list):
        return web.json_response({"error": "Ocekivana je lista 'facts'."}, status=400)

    filtered = [fact for fact in facts if isinstance(fact, str) and contains_cat_word(fact)]

    return web.json_response({"facts": filtered})


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_post("/facts", facts_handler)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), port=8087)
