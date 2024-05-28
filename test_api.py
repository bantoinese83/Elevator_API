# test_api.py
import pytest
from flask_testing import TestCase
from api import elevator


class TestElevatorAPI(TestCase):
    def create_app(self):
        return elevator

    def test_request_elevator(self):
        self._test_valid_request()
        self._test_invalid_request()

    def _test_valid_request(self):
        response = self.client.post(
            "/elevator/request_elevator",
            json={"current_floor": 0, "destination_floors": [2], "num_people": 1},
        )
        assert response.status_code == 200
        assert response.json == {"status": "success", "message": "Request received"}

    def _test_invalid_request(self):
        response = self.client.post(
            "/elevator/request_elevator",
            json={"current_floor": 0, "destination_floors": [20], "num_people": 1},
        )
        assert response.status_code == 400
        assert response.json == {"status": "error", "message": "Floor out of range"}

    def test_status(self):
        response = self.client.get("/elevator/status")
        assert response.status_code == 200
        assert isinstance(response.json, list)
        for elevator_status in response.json:
            self._validate_elevator_status(elevator_status)

    @staticmethod
    def _validate_elevator_status(elevator_status):
        assert "id" in elevator_status
        assert "current_floor" in elevator_status
        assert "destination_floors" in elevator_status
        assert "direction" in elevator_status
        assert "door_open" in elevator_status
        assert "current_load" in elevator_status
        assert "maintenance" in elevator_status


@pytest.fixture(scope="module")
def test_client():
    with elevator.test_client() as testing_client:
        with elevator.app_context():
            yield testing_client
