import asyncio
from aiohttp import ClientSession
from typing import Any


async def call_service(
    session: ClientSession, port: int, endpoint: str, payload: Any
) -> Any:
    url = f"http://localhost:{port}{endpoint}"
    async with session.post(url, json=payload) as response:
        data = await response.json()
        return response.status, data


async def main() -> None:
    numbers = [2, 4, 6, 8]

    async with ClientSession() as session:
        print("Konkurentno slanje zahtjeva za zbroj i umnozak...")
        sum_task = asyncio.create_task(call_service(session, 8083, "/zbroj", numbers))
        product_task = asyncio.create_task(
            call_service(session, 8084, "/umnozak", numbers)
        )

        (sum_status, sum_response), (prod_status, prod_response) = await asyncio.gather(
            sum_task, product_task
        )

        print("  /zbroj ->", sum_status, sum_response)
        print("  /umnozak ->", prod_status, prod_response)

        if sum_status != 200 or prod_status != 200:
            print("Neuspjeh u izracunu zbroja ili umnozka, prekidam.")
            return

        print("\nSekvencijalno slanje zahtjeva za kolicnik...")
        quotient_payload = {
            "zbroj": sum_response["zbroj"],
            "umnozak": prod_response["umnozak"],
        }
        quotient_status, quotient_response = await call_service(
            session, 8085, "/kolicnik", quotient_payload
        )

        print("  /kolicnik ->", quotient_status, quotient_response)


if __name__ == "__main__":
    asyncio.run(main())
