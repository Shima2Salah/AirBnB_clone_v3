#!/usr/bin/python3
"""
syart route api
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """ if okay return okay"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """ count each object """
    stats = {}
    stats['amenities'] = storage.count("Amenity")
    stats['cities'] = storage.count("City")
    stats['places'] = storage.count("Place")
    stats['reviews'] = storage.count("Review")
    stats['states'] = storage.count("State")
    stats['users'] = storage.count("User")
    return jsonify(stats)
