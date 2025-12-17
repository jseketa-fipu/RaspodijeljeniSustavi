import json
from typing import List, Dict, Any
from aiohttp import web
from typing_extensions import Annotated
from decimal import Decimal, InvalidOperation
from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    PositiveInt,
    field_validator,
)

# using Any instead of str | int | float
# pydantic model validation takes care of actual validation
PROIZVODI: List[Dict[str, Any]] = [
    {"id": 1, "naziv": "Laptop", "cijena": 5000.0, "kolicina": 2},
    {"id": 2, "naziv": "Miš", "cijena": 100.0, "kolicina": 15},
    {"id": 3, "naziv": "Tipkovnica", "cijena": 200.0, "kolicina": 12},
    {"id": 4, "naziv": "Monitor", "cijena": 1000.0, "kolicina": 7},
    {"id": 5, "naziv": "Slušalice", "cijena": 50.0, "kolicina": 100},
]


class ProductInput(BaseModel):
    id: PositiveInt
    naziv: str
    cijena: Annotated[
        Decimal,
        Field(
            strict=True,
            gt=0,
            decimal_places=2,
            description="Must be positive with a maximum of 2 decimal places.",
        ),
    ]
    kolicina: PositiveInt

    @field_validator("cijena", mode="before")
    @classmethod
    # typed cls to Any, because couldn't be bothered to type it directly to a class
    def cast_decimal(cls: Any, value: Any) -> Decimal:
        try:
            return Decimal(str(value))
        except (InvalidOperation, TypeError, ValueError) as exception:
            raise ValueError("Cijena mora biti broj.") from exception


async def get_products_handler(request: web.Request) -> web.Response:
    return web.json_response(PROIZVODI)


async def post_products_handler(request: web.Request) -> web.Response:
    try:
        product_new = await request.json()
    except Exception:
        # if the conversion to json fails, this exception gets triggered
        return web.json_response(
            {"error": "Request must contain a valid JSON object."}, status=400
        )

    try:
        product_input = ProductInput(**product_new)
    except ValidationError as exception:
        # double stars map the dictionary to the ProductInput pydantic's model
        # raises exception if the validation in the model fails
        # using passing exception in json.loads() covers the decimal types to be
        # properly serialized
        return web.json_response(
            {"error": json.loads(exception.json())},
            status=400,
        )

    for product in PROIZVODI:
        if product["id"] == product_input.id:
            product.update(
                {
                    "naziv": product_input.naziv,
                    "cijena": float(product_input.cijena),
                    "kolicina": product["kolicina"] + product_input.kolicina,
                }
            )
            break
    else:
        PROIZVODI.append(
            {
                "id": product_input.id,
                "naziv": product_input.naziv,
                "cijena": float(product_input.cijena),
                "kolicina": product_input.kolicina,
            }
        )

    print("Updated list of products:", PROIZVODI)
    return web.json_response(PROIZVODI)


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/proizvodi", get_products_handler)
    app.router.add_post("/proizvodi", post_products_handler)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), port=8081)
