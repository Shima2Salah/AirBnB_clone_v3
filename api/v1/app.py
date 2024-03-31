#!/usr/bin/python3
"""
to get and run api flask
"""
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def shut(exec):
    """ close session storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ page not found error handling """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(getenv('HBNB_API_HOST'), getenv('HBNB_API_PORT'), threaded=True)
