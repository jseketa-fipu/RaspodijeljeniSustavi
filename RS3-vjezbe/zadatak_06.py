# type: ignore
# Ruff doesn't allow multiple imports in the same line
# According to PEP 8, "imports should usually be on separate lines."
import asyncio
import time


async def fetch_data(param):
    print(f"Nešto radim s {param}...")
    await asyncio.sleep(param)
    print(f"Dovršio sam s {param}.")
    return f"Rezultat za {param}"


async def main():
    task1 = asyncio.create_task(fetch_data(1))  # schedule
    task2 = asyncio.create_task(fetch_data(2))  # schedule
    result1 = await task1
    # start of code addition
    # just keep the async main alive enough with sleep, so the task2
    # has the time to finish
    # taks1 needs 1 second, taks 2 needs 2 seconds
    # add a sleep that lasts longer than 1 second
    await asyncio.sleep(1.1)
    # end of code addition
    print("Fetch 1 uspješno završen.")
    return [result1]


t1 = time.perf_counter()
results = asyncio.run(main())  # pokretanje event loop-a
t2 = time.perf_counter()
print(results)
print(f"Vrijeme izvođenja {t2 - t1:.2f} sekunde")
