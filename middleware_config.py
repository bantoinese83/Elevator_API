# middleware_config.py
from flask_cors import CORS
from flask import jsonify


def init_cors(app):
    # Allow requests from any origin, with any headers, and any HTTP method
    CORS(app, resources={r"/*": {"origins": "*"}})
    return app


def handle_errors(app):
    @app.errorhandler(Exception)
    def handle_error(error):
        response = {"status": "error", "message": str(error)}
        return jsonify(response), 500

    return app
