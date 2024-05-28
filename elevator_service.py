# elevator_service.py
import logging
import queue
import threading
import time

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Request:
    def __init__(self, current_floor, destination_floors, total_floors, num_people=1):
        if not (0 <= current_floor < total_floors) or not all(
            0 <= floor < total_floors for floor in destination_floors
        ):
            raise ValueError("Floor out of range")
        self.current_floor = current_floor
        self.destination_floors = destination_floors
        self.num_people = num_people
        self.direction = "up" if destination_floors[0] > current_floor else "down"


class Elevator:
    def __init__(self, _id, total_floors, capacity=10):
        self.id = _id
        self.current_floor = 0
        self.destination_floors = []
        self.total_floors = total_floors
        self.direction = None  # None, "up", or "down"
        self.door_open = False
        self.capacity = capacity
        self.current_load = 0
        self.maintenance = False

    def move(self):
        if self.destination_floors:
            if self.current_floor < self.destination_floors[0]:
                self.current_floor += 1
                self.direction = "up"
            elif self.current_floor > self.destination_floors[0]:
                self.current_floor -= 1
                self.direction = "down"
            else:
                self.destination_floors.pop(0)
                self.door_open = True
                time.sleep(1)  # time to open/close doors
                self.door_open = False
                if self.destination_floors:
                    self.direction = (
                        "up"
                        if self.destination_floors[0] > self.current_floor
                        else "down"
                    )
                else:
                    self.direction = None

                # Move to the next destination floor if available
                if self.destination_floors:
                    if self.destination_floors[0] > self.current_floor:
                        self.current_floor += 1
                        self.direction = "up"
                    elif self.destination_floors[0] < self.current_floor:
                        self.current_floor -= 1
                        self.direction = "down"
                else:
                    self.direction = None

    def add_request(self, _request):
        if self.current_load + _request.num_people <= self.capacity:
            self.current_load += _request.num_people
            for floor in _request.destination_floors:
                if floor not in self.destination_floors:
                    self.destination_floors.append(floor)
            self.destination_floors.sort()
            return True
        return False

    def status(self):
        return {
            "id": self.id,
            "current_floor": self.current_floor,
            "destination_floors": self.destination_floors,
            "direction": self.direction,
            "door_open": self.door_open,
            "current_load": self.current_load,
            "maintenance": self.maintenance,
        }


class ElevatorController:
    def __init__(self, num_elevators, total_floors):
        self.elevators = [Elevator(i, total_floors) for i in range(num_elevators)]
        self.total_floors = total_floors
        self.request_queue = queue.PriorityQueue()

    def request_elevator(self, _request):
        self.request_queue.put((_request.num_people, _request))

    def find_best_elevator(self, _request):
        best_elevator = None
        min_cost = float("inf")

        for _elevator in self.elevators:
            if not _elevator.maintenance and (
                _elevator.direction == _request.direction or _elevator.direction is None
            ):
                distance = abs(_elevator.current_floor - _request.current_floor)
                cost = distance + len(_elevator.destination_floors)
                if (
                    cost < min_cost
                    and _elevator.current_load + _request.num_people
                    <= _elevator.capacity
                ):
                    min_cost = cost
                    best_elevator = _elevator

        if best_elevator is None:
            best_elevator = min(
                (
                    e
                    for e in self.elevators
                    if not e.maintenance
                    and e.current_load + _request.num_people <= e.capacity
                ),
                key=lambda e: len(e.destination_floors),
                default=None,
            )

        return best_elevator

    def handle_requests(self):
        while True:
            _, _request = self.request_queue.get()
            best_elevator = self.find_best_elevator(_request)
            if best_elevator:
                if not best_elevator.add_request(_request):
                    logging.warning(f"Elevator {best_elevator.id} is at full capacity.")
            self.request_queue.task_done()

    def step(self):
        for _elevator in self.elevators:
            _elevator.move()

    def status(self):
        return [_elevator.status() for _elevator in self.elevators]

    def run(self):
        threading.Thread(target=self.handle_requests, daemon=True).start()
        while True:
            self.step()
            logging.info("Elevator Status: %s", self.status())
            time.sleep(1)


def monitor_elevator_reach_destination(elevator_id, destination_floor):
    while True:
        for _elevator in controller.elevators:
            if _elevator.id == elevator_id:
                if _elevator.current_floor == destination_floor:
                    logging.info(
                        f"Elevator {elevator_id} reached destination floor {destination_floor}"
                    )
                    return
                break
        time.sleep(1)


controller = ElevatorController(num_elevators=3, total_floors=10)
