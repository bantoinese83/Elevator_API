# Elevator API

## Description

This project provides a simple Elevator API implemented in Python using Flask. It allows users to request an elevator and check the status of elevators.

## Installation

1. Clone the repository: git clone https://github.com/yourusername/elevator-api.git
2. Install the required packages:
```bash
pip install -r requirements.txt
```
## Usage

1. Start the server:
2. Run the following command:
```bash
python app.py
```
- Open your browser and navigate to http://localhost:5000
- You can now make requests to the API.


## API Endpoints

- `POST /elevator/request_elevator`: Request an elevator. The body of the request should be a JSON object with the following properties:
  - `current_floor`: The current floor of the user.
  - `destination_floors`: A list of destination floors.
  - `num_people`: The number of people (optional, default is 1).

- `GET /elevator/status`: Get the status of all elevators. The response is a list of elevator status objects.

## Testing

To run the tests, use the following command:
```bash
pytest
```

