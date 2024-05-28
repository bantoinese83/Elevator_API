# api.py
from flask import Flask, request
from flask_restx import Api, Resource, fields

from elevator_service import controller, Request

elevator = Flask(__name__)
api = Api(
    elevator,
    version="1.0",
    title="Elevator API",
    description="A simple Elevator API",
)

ns = api.namespace("elevator", description="Elevator operations")

request_model = api.model(
    "Request",
    {
        "current_floor": fields.Integer(required=True, description="The current floor"),
        "destination_floors": fields.List(
            fields.Integer, required=True, description="The destination floors"
        ),
        "num_people": fields.Integer(
            required=False, description="The number of people", default=1
        ),
    },
)


@ns.route("/request_elevator")
class ElevatorRequest(Resource):
    @ns.expect(request_model)
    @ns.response(200, "Request received")
    @ns.response(400, "Validation Error")
    def post(self):
        data = request.json
        try:
            req = Request(
                current_floor=data["current_floor"],
                destination_floors=data["destination_floors"],
                total_floors=controller.total_floors,
                num_people=data.get("num_people", 1),
            )
            controller.request_elevator(req)
            return {"status": "success", "message": "Request received"}, 200
        except ValueError as e:
            return {"status": "error", "message": str(e)}, 400


@ns.route("/status")
class ElevatorStatus(Resource):
    @ns.response(200, "Success")
    def get(self):
        return controller.status(), 200
