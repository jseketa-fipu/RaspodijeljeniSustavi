import asyncio
from aiohttp import ClientSession


async def call_service(
    session: ClientSession, method: str, port: int, path: str, *, payload=None
):
    url = f"http://localhost:{port}{path}"
    async with session.request(method, url, json=payload) as response:
        return response.status, await response.json()


async def main() -> None:
    amount = 10
    async with ClientSession() as session:
        print(f"Zahtjev na cat_microservice za {amount} cinjenica...")
        cats_status, cats_response = await call_service(
            session, "GET", 8086, f"/cat/{amount}"
        )
        print("  Odgovor:", cats_status, cats_response)

        if cats_status != 200 or "facts" not in cats_response:
            print("Neuspjeh u dohvaćanju činjenica, prekidam.")
            return

        facts_payload = {"facts": cats_response["facts"]}
        print("\nSlanje činjenica na cat_fact_check mikroservis...")
        filtered_status, filtered_response = await call_service(
            session, "POST", 8087, "/facts", payload=facts_payload
        )
        print("  Odgovor:", filtered_status, filtered_response)


if __name__ == "__main__":
    asyncio.run(main())
