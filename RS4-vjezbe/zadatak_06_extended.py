# type: ignore
import asyncio
import random
from dataclasses import dataclass
from typing import Optional

import curses


FAILURE_PROBABILITY = 0.25
TECHNICIAN_COUNT = 3
TECH_SPEED_KM_PER_SEC = 10  # fake speed for demo scaling


@dataclass
class WeatherStation:
    station_id: int
    name: str
    distance_km: float
    importance: int  # 1–3 (3 = most important)
    is_online: bool = True
    last_failure_time: Optional[float] = None

    # UI fields
    status: str = "ONLINE"  # ONLINE / DOWN / WAITING / EN ROUTE / REPAIRING
    last_temp: Optional[float] = None
    last_event: str = ""
    assigned_tech: Optional[int] = None

    # Ticket flag: whether there is an open incident for this station
    has_open_ticket: bool = False


@dataclass
class TechnicianState:
    tech_id: int
    status: str = "IDLE"  # IDLE / TRAVEL / REPAIR
    station_name: Optional[str] = None
    last_event: str = ""


def compute_priority(station: WeatherStation, now: float) -> float:
    if station.last_failure_time is None:
        downtime = 0.0
    else:
        downtime = now - station.last_failure_time
    # bigger importance & longer downtime => more urgent (i.e. more negative)
    return -(station.importance * 1000 + downtime)


async def station_process(station: WeatherStation) -> None:
    loop = asyncio.get_running_loop()
    while True:
        await asyncio.sleep(random.uniform(1, 3))

        if station.is_online:
            if random.random() < FAILURE_PROBABILITY:
                station.is_online = False
                station.last_failure_time = loop.time()
                station.status = "DOWN"
                station.last_event = "FAILED"
            else:
                temp = random.uniform(20, 25)
                station.last_temp = temp
                station.status = "ONLINE"
                station.last_event = f"Reading {temp:.1f} °C"
        else:
            if station.assigned_tech is None and not station.has_open_ticket:
                station.status = "DOWN"
                station.last_event = "DOWN (no tech yet)"
            # else: monitor / tech worker updates status


async def monitor_stations(
    stations: list[WeatherStation],
    incident_queue: asyncio.PriorityQueue,
    check_interval: float = 1.0,
) -> None:
    loop = asyncio.get_running_loop()
    while True:
        now = loop.time()
        for st in stations:
            # Only create one incident per failure
            if not st.is_online and not st.has_open_ticket:
                prio = compute_priority(st, now)
                st.has_open_ticket = True
                st.status = "WAITING"
                st.last_event = "Incident queued"
                await incident_queue.put((prio, now, st))
        await asyncio.sleep(check_interval)


async def technician_worker(
    tech_state: TechnicianState,
    incident_queue: asyncio.PriorityQueue,
) -> None:
    tech_id = tech_state.tech_id

    while True:
        prio, created_at, station = await incident_queue.get()

        # If station is already back online, this ticket is obsolete
        if station.is_online:
            station.has_open_ticket = False
            station.assigned_tech = None
            station.status = "ONLINE"
            station.last_event = "Incident obsolete"
            incident_queue.task_done()
            continue

        station.assigned_tech = tech_id
        station.status = "EN ROUTE"
        station.last_event = f"Tech {tech_id} dispatched"

        tech_state.status = "TRAVEL"
        tech_state.station_name = station.name
        tech_state.last_event = f"Heading to {station.name}"

        travel_time = station.distance_km / TECH_SPEED_KM_PER_SEC
        await asyncio.sleep(travel_time)

        tech_state.status = "REPAIR"
        tech_state.last_event = f"Repairing {station.name}"
        station.status = "REPAIRING"
        station.last_event = f"Tech {tech_id} repairing"

        repair_time = random.uniform(1, 3)
        await asyncio.sleep(repair_time)

        station.is_online = True
        station.last_failure_time = None
        station.assigned_tech = None
        station.has_open_ticket = False
        station.status = "ONLINE"
        station.last_event = f"Repaired by tech {tech_id}"

        tech_state.status = "IDLE"
        tech_state.station_name = None
        tech_state.last_event = "Idle"

        incident_queue.task_done()


def status_color_pair(status: str) -> int:
    """
    Map status -> curses color pair index.
    We'll define:
      1: green   (ONLINE)
      2: red     (DOWN/WAITING)
      3: yellow  (EN ROUTE/REPAIRING)
      4: cyan    (headings)
    """
    s = status.upper()
    if s == "ONLINE":
        return 1
    if s in ("DOWN", "WAITING"):
        return 2
    if s in ("EN ROUTE", "REPAIRING"):
        return 3
    return 0  # default terminal color


async def display_loop_curses(
    stdscr,
    stations: list[WeatherStation],
    tech_states: list[TechnicianState],
    interval: float = 0.5,
) -> None:
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    curses.init_pair(4, curses.COLOR_CYAN, -1)

    while True:
        stdscr.erase()

        # Title
        stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
        stdscr.addstr(0, 0, "Weather Station Maintenance Simulation")
        stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)

        row = 2
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(row, 0, "Stations:")
        stdscr.attroff(curses.color_pair(4))
        row += 1

        header = (
            f"{'ID':>2}  {'Name':<18}  {'Status':<12}  {'Temp':>6}  {'Tech':>4}  Info"
        )
        stdscr.addstr(row, 0, header)
        row += 1
        stdscr.addstr(row, 0, "-" * len(header))
        row += 1

        # Stations
        for st in stations:
            temp_str = f"{st.last_temp:.1f}" if st.last_temp is not None else "--"
            tech_str = str(st.assigned_tech) if st.assigned_tech else "-"

            col = 0
            # ID
            stdscr.addstr(row, col, f"{st.station_id:>2}")
            col += 2
            # 2 spaces
            stdscr.addstr(row, col, "  ")
            col += 2
            # Name
            stdscr.addstr(row, col, f"{st.name:<18.18}")
            col += 18
            # 2 spaces
            stdscr.addstr(row, col, "  ")
            col += 2
            # Colored status (12 chars)
            status_pair = status_color_pair(st.status)
            if status_pair:
                stdscr.attron(curses.color_pair(status_pair))
            stdscr.addstr(row, col, f"{st.status:<12}")
            if status_pair:
                stdscr.attroff(curses.color_pair(status_pair))
            col += 12
            # Temp, tech, info
            tail = f"  {temp_str:>6}  {tech_str:>4}  {st.last_event}"
            stdscr.addstr(row, col, tail)

            row += 1

        row += 1
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(row, 0, "Technicians:")
        stdscr.attroff(curses.color_pair(4))
        row += 1

        thead = f"{'ID':>2}  {'Status':<8}  {'Station':<18}  Info"
        stdscr.addstr(row, 0, thead)
        row += 1
        stdscr.addstr(row, 0, "-" * len(thead))
        row += 1

        for tech in tech_states:
            station_name = tech.station_name or "-"
            line = f"{tech.tech_id:>2}  {tech.status:<8}  {station_name:<18.18}  {tech.last_event}"
            col_status = (
                3
                if tech.status in ("TRAVEL", "REPAIR")
                else 1 if tech.status == "IDLE" else 0
            )
            if col_status:
                stdscr.attron(curses.color_pair(col_status))
                stdscr.addstr(row, 0, line)
                stdscr.attroff(curses.color_pair(col_status))
            else:
                stdscr.addstr(row, 0, line)
            row += 1

        stdscr.refresh()
        await asyncio.sleep(interval)


async def async_main(stdscr) -> None:
    stations = [
        WeatherStation(1, "Zagreb–Centar", 10, importance=3),
        WeatherStation(2, "Rijeka–Luka", 50, importance=2),
        WeatherStation(3, "Osijek–Istočni", 80, importance=1),
        WeatherStation(4, "Split–Aerodrom", 30, importance=3),
        WeatherStation(5, "Pula–Obala", 60, importance=2),
    ]

    incident_queue: asyncio.PriorityQueue = asyncio.PriorityQueue()

    station_tasks = [asyncio.create_task(station_process(st)) for st in stations]
    monitor_task = asyncio.create_task(monitor_stations(stations, incident_queue))

    tech_states = [TechnicianState(tech_id=i) for i in range(1, TECHNICIAN_COUNT + 1)]
    tech_tasks = [
        asyncio.create_task(technician_worker(ts, incident_queue)) for ts in tech_states
    ]

    display_task = asyncio.create_task(
        display_loop_curses(stdscr, stations, tech_states)
    )

    try:
        await asyncio.sleep(60)  # run for 60 seconds
    finally:
        for t in station_tasks + tech_tasks + [monitor_task, display_task]:
            t.cancel()
        await asyncio.gather(
            *station_tasks,
            *tech_tasks,
            monitor_task,
            display_task,
            return_exceptions=True,
        )


def curses_main(stdscr):
    return asyncio.run(async_main(stdscr))


if __name__ == "__main__":
    curses.wrapper(curses_main)
