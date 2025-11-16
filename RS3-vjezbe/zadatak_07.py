# type: ignore
import asyncio


async def timer(name, delay):
    print(f"[{name}] started (RUNNING)")  # coroutine just started
    for i in range(delay, 0, -1):
        print(f"{name}: {i} sekundi preostalo...")

        print(f"[{name}] about to await sleep (WAITING)")
        await asyncio.sleep(1)
        print(f"[{name}] resumed after sleep (RUNNING)")

    print(f"{name}: Vrijeme je isteklo!")
    print(f"[{name}] finished (DONE)")  # coroutine is done


async def main():
    print("[main] creating tasks")
    timers = [
        asyncio.create_task(timer("Timer 1", 3)),
        asyncio.create_task(timer("Timer 2", 5)),
        asyncio.create_task(timer("Timer 3", 7)),
    ]

    print("[main] tasks created, about to await asyncio.gather(...) (WAITING)")
    await asyncio.gather(*timers)
    print("[main] asyncio.gather finished, main is DONE")


asyncio.run(main())
