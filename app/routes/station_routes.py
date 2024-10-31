from flask import Blueprint, jsonify, request
from models import Station, DiningHall, db
from schemas import StationSchema

# register blueprint and create schemas
stations_bp = Blueprint('stations', __name__)
station_schema = StationSchema()
stations_schema = StationSchema(many=True)

# POST /api/v1/stations: Add a new station
@stations_bp.route('/stations', methods=['POST'])
def create_station():
    """
    Create a new station
    ---
    tags:
      - Stations
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Station
          required:
            - name
            - dining_hall_id
          properties:
            name:
              type: string
              description: The name of the station
              example: "Grill Station"
            dining_hall_id:
              type: integer
              description: The ID of the dining hall associated with this station
              example: 1
    responses:
      201:
        description: Station created
        schema:
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: "Grill Station"
            dining_hall_id:
              type: integer
              example: 1
      400:
        description: Invalid input or dining hall not found
    """
    data = request.get_json()
    name = data.get('name')
    dining_hall_id = data.get('dining_hall_id')

    if not name or not dining_hall_id:
        return jsonify({"error": "Name and dining_hall_id are required"}), 400

    # Check if the dining hall exists
    dining_hall = db.session.query(DiningHall).get(dining_hall_id)
    if not dining_hall:
        return jsonify({"error": "Dining hall not found"}), 400

    new_station = Station(name=name, dining_hall_id=dining_hall_id)
    db.session.add(new_station)
    db.session.commit()

    return station_schema.jsonify(new_station), 201

@stations_bp.route('/stations/<int:id>', methods=['GET'])
def get_station(id):
    """
    Retrieve detailed information about a specific station
    ---
    tags:
      - Stations
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: ID of the station
        example: 1
    responses:
      200:
        description: A station
        schema:
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: "Grill Station"
            dining_hall_id:
              type: integer
              example: 1
            _links:
              type: object
              properties:
                collection:
                  type: string
                  example: "/api/v1/stations"
                self:
                  type: string
                  example: "/api/v1/stations/{id}"
                update:
                  type: string
                  example: "/api/v1/stations/{id}"
      404:
        description: Station not found
    """
    station = db.session.query(Station).get(id)
    if not station:
        return jsonify({"error": "Station not found"}), 404
    return station_schema.jsonify(station), 200
