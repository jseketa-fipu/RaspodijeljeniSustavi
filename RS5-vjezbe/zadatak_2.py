from typing import List
from aiohttp import web
from pydantic import BaseModel, ValidationError, condecimal, constr, PositiveInt

PROIZVODI: List[dict] = [
    {"id": 1, "naziv": "Laptop", "cijena": 5000.0, "kolicina": 2},
    {"id": 2, "naziv": "Miš", "cijena": 100.0, "kolicina": 15},
    {"id": 3, "naziv": "Tipkovnica", "cijena": 200.0, "kolicina": 12},
    {"id": 4, "naziv": "Monitor", "cijena": 1000.0, "kolicina": 7},
    {"id": 5, "naziv": "Slušalice", "cijena": 50.0, "kolicina": 100},
]


class ProductInput(BaseModel):
    id: PositiveInt
    naziv: constr(strip_whitespace=True, min_length=1)
    cijena: condecimal(gt=0, decimal_places=2)
    kolicina: PositiveInt


async def get_proizvodi(request: web.Request) -> web.Response:
    return web.json_response(PROIZVODI)


async def post_proizvodi(request: web.Request) -> web.Response:
    try:
        novi_proizvod = await request.json()
    except Exception:
        return web.json_response(
            {"error": "Tijelo zahtjeva mora biti valjani JSON objekt."}, status=400
        )

    if not isinstance(novi_proizvod, dict):
        return web.json_response(
            {"error": "JSON tijelo mora biti rječnik s podacima o proizvodu."},
            status=400,
        )

    try:
        product_input = ProductInput(**novi_proizvod)
    except ValidationError as exc:
        return web.json_response({"error": exc.errors()}, status=400)

    proizvod_id = product_input.id
    existing = next((p for p in PROIZVODI if p["id"] == proizvod_id), None)
    if existing:
        existing["naziv"] = product_input.naziv
        existing["cijena"] = float(product_input.cijena)
        existing["kolicina"] += product_input.kolicina
    else:
        PROIZVODI.append(
            {
                "id": product_input.id,
                "naziv": product_input.naziv,
                "cijena": float(product_input.cijena),
                "kolicina": product_input.kolicina,
            }
        )

    print("Ažurirana lista proizvoda:", PROIZVODI)
    return web.json_response(PROIZVODI)


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/proizvodi", get_proizvodi)
    app.router.add_post("/proizvodi", post_proizvodi)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), port=8081)
