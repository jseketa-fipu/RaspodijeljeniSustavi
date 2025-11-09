import asyncio

lista_brojeva: list[int] = [i for i in range(1, 11)]


# define the aync function
# simulate waiting for data by using the asyncio.sleep function
async def dohvati_podatke() -> list[int]:
    await asyncio.sleep(3)
    print("Podaci dohvaćeni.")

    return lista_brojeva


# actually run the defined function and assign the return value to a variable
podaci = asyncio.run(dohvati_podatke())

print(podaci)
