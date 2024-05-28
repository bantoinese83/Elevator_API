import logging
import threading

from flask import Flask

from api import elevator
from middleware_config import init_cors, handle_errors
from elevator_service import controller, monitor_elevator_reach_destination

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
app = Flask(__name__)
init_cors(app)
handle_errors(app)


if __name__ == "__main__":
    threading.Thread(target=controller.run, daemon=True).start()
    elevator.run(debug=True)

    # Start a thread to monitor elevator reaching destination
    threading.Thread(
        target=monitor_elevator_reach_destination, args=(0, 5), daemon=True
    ).start()
