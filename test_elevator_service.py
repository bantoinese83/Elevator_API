# test_elevator_service.py
import threading
import unittest
import unittest.mock

import pytest

from elevator_service import (
    Request,
    Elevator,
    ElevatorController,
)


class TestElevatorService(unittest.TestCase):
    def test_request(self):
        self._test_valid_request()
        self._test_invalid_request()

    @staticmethod
    def _test_valid_request():
        request = Request(0, [2], 10, 1)
        assert request.current_floor == 0
        assert request.destination_floors == [2]
        assert request.num_people == 1
        assert request.direction == "up"

    @staticmethod
    def _test_invalid_request():
        with pytest.raises(ValueError):
            Request(0, [20], 10, 1)  # Invalid floor

    def test_elevator(self):
        self._test_elevator_initialization()
        self._test_elevator_request()
        self._test_elevator_move()

    @staticmethod
    def _test_elevator_initialization():
        elevator = Elevator(0, 10)
        assert elevator.id == 0
        assert elevator.current_floor == 0
        assert elevator.destination_floors == []
        assert elevator.direction is None
        assert not elevator.door_open
        assert elevator.current_load == 0
        assert not elevator.maintenance

    @staticmethod
    def _test_elevator_request():
        elevator = Elevator(0, 10)
        request = Request(0, [2], 10, 1)
        assert elevator.add_request(request)
        assert elevator.destination_floors == [2]
        assert elevator.current_load == 1

    @staticmethod
    def _test_elevator_move():
        elevator = Elevator(0, 10)
        request = Request(0, [2], 10, 1)
        elevator.add_request(request)
        elevator.move()
        assert elevator.current_floor == 1
        assert elevator.direction == "up"

    def test_elevator_controller(self):
        self._test_elevator_controller_initialization()
        self._test_elevator_controller_request()
        self._test_elevator_controller_best_elevator()

    @staticmethod
    def _test_elevator_controller_initialization():
        controller = ElevatorController(3, 10)
        assert len(controller.elevators) == 3
        assert controller.total_floors == 10

    @staticmethod
    def _test_elevator_controller_request():
        controller = ElevatorController(3, 10)
        request = Request(0, [2], 10, 1)
        controller.request_elevator(request)
        assert not controller.request_queue.empty()

    @staticmethod
    def _test_elevator_controller_best_elevator():
        controller = ElevatorController(3, 10)
        request = Request(0, [2], 10, 1)
        best_elevator = controller.find_best_elevator(request)
        assert best_elevator is not None

    def test_monitor_elevator_reach_destination(self):
        controller = ElevatorController(3, 10)
        elevator_id = 0
        destination_floor = 2

        # Mock the monitor_elevator_reach_destination function
        with unittest.mock.patch(
            "elevator_service.monitor_elevator_reach_destination"
        ) as mock_monitor:
            # Start the mock function in a new thread
            threading.Thread(
                target=mock_monitor,
                args=(elevator_id, destination_floor),
                daemon=True,
            ).start()

            # Set the elevator's current floor to the destination floor
            controller.elevators[elevator_id].current_floor = destination_floor

            # Check that the mock function was called with the correct arguments
            mock_monitor.assert_called_with(elevator_id, destination_floor)
