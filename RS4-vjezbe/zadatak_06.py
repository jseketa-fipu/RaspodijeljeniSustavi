# zadatak 6: Simulacija raspodijeljenog sustava za dohvaćanje i obradu vremenskih podataka
import asyncio
import random
from typing import Optional, List


async def fetch_weather_data(station_id: int) -> float:
    """
    Simulate a weather microservice for one station.
    - Random delay between 1 and 5 seconds
    - Random temperature between 20 and 25 °C
    """
    delay = random.uniform(1, 5)
    await asyncio.sleep(delay)

    temperature = random.uniform(20, 25)
    print(f"Station {station_id} responded in {delay:.2f}s with {temperature:.2f}°C")
    return temperature


async def fetch_with_timeout(station_id: int, timeout: float = 2.0) -> Optional[float]:
    """
    Wrap fetch_weather_data with an external timeout.
    - If the station responds within `timeout`, return its temperature (float)
    - If it times out, handle TimeoutError and return None
    """
    try:
        return await asyncio.wait_for(fetch_weather_data(station_id), timeout=timeout)
    except asyncio.TimeoutError:
        print(
            f"Station {station_id} timed out (>{timeout:.2f}s) – ignoring this station."
        )
        return None


async def main() -> None:
    num_stations = 10

    # Create 10 tasks, one per weather station
    tasks: List[asyncio.Task[Optional[float]]] = [
        asyncio.create_task(fetch_with_timeout(station_id))
        for station_id in range(1, num_stations + 1)
    ]

    # Wait for all of them to finish (some will return None because of timeout)
    results: List[Optional[float]] = await asyncio.gather(*tasks)

    # Filter out stations that timed out
    successful_temps: List[float] = [t for t in results if t is not None]

    print("\nSummary:")
    if successful_temps:
        avg_temp = sum(successful_temps) / len(successful_temps)
        print(
            f"Received data from {len(successful_temps)}/{num_stations} stations.\n"
            f"Average temperature: {avg_temp:.2f}°C"
        )
    else:
        print(
            "No station responded within the timeout. "
            "Cannot compute average temperature."
        )


if __name__ == "__main__":
    asyncio.run(main())
