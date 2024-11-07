from flask import Blueprint, jsonify, request
from models import DiningHall, Station, db
from schemas import DiningHallSchema, StationSchema

# register blueprint and create schemas
dining_halls_bp = Blueprint('dining_halls', __name__)
dining_hall_schema = DiningHallSchema()
dining_halls_schema = DiningHallSchema(many=True)

# POST: /api/v1/dining_halls: Add a new dining hall
@dining_halls_bp.route('/dining_halls', methods=['POST'])
def add_dining_hall():
    """
    Add a new dining hall
    ---
    tags:
      - Dining Halls
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: DiningHall
          required:
            - name
          properties:
            name:
              type: string
              description: The name of the dining hall
              example: "John Jay"
    responses:
      201:
        description: Dining hall added
        schema:
          properties:
            id:
              type: integer
              example: 1
            message:
              type: string
              example: "Dining hall added"
      400:
        description: Name is required
      409:
        description: Dining hall with the same name already exists
    """
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({"error": "Name is required"}), 400

    # Check if a dining hall with the same name already exists
    existing_dining_hall = DiningHall.query.filter_by(name=name).first()
    if existing_dining_hall:
        return jsonify({"error": "Dining hall with the same name already exists"}), 409

    new_dining_hall = DiningHall(name=name)
    db.session.add(new_dining_hall)
    db.session.commit()

    return jsonify({"id": new_dining_hall.id, "message": "Dining hall added"}), 201

# GET /api/v1/dining_halls: Retrieve a list of all dining halls
@dining_halls_bp.route('/dining_halls', methods=['GET'])
def get_dining_halls():
    """
    Retrieve a list of all dining halls
    ---
    tags:
      - Dining Halls
    parameters:
      - name: name
        in: query
        type: string
        description: Filter by dining hall name
        example: "John Jay"
    responses:
      200:
        description: A list of dining halls
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: "John Jay"
              station:
                type: string
                example: "Grill"
              _links:
                type: object
                properties:
                  self:
                    type: string
                    example: "/api/v1/dining_halls/1"
                  collection:
                    type: string
                    example: "/api/v1/dining_halls"
    """
    name_filter = request.args.get('name')

    query = db.session.query(DiningHall)
    if name_filter:
        query = query.filter(DiningHall.name.like(f"%{name_filter}%"))

    dining_halls = query.all()
    dining_halls_data = [
        {
            "id": dh.id,
            "name": dh.name,
            "_links": {
                "self": f"/api/v1/dining_halls/{dh.id}",
                "collection": "/api/v1/dining_halls"
            }
        } for dh in dining_halls
    ]

    # TODO: change this to dining_hall_schema.jsonify
    return jsonify(dining_halls_data), 200

# GET /api/v1/dining_halls/{id}/stations: Retrieve all the stations within a specific dining hall
@dining_halls_bp.route('/dining_halls/<int:id>/stations', methods=['GET'])
def get_stations(id):
    """
    Retrieve all stations within a specific dining hall
    ---
    tags:
      - Dining Halls
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the dining hall
        example: 1
      - name: name
        in: query
        type: string
        description: Filter by station name
        example: "Grill Station"
    responses:
      200:
        description: A list of stations within the specified dining hall
        schema:
          type: array
          items:
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
                  self:
                    type: string
                    example: "/api/v1/dining_halls/1/stations/1"
                  dining_hall:
                    type: string
                    example: "/api/v1/dining_halls/1"
      404:
        description: Dining hall not found
    """
    # Query for the dining hall to ensure it exists
    dining_hall = DiningHall.query.get(id)
    if not dining_hall:
        return jsonify({"error": "Dining hall not found"}), 404

    # Get the station name filter from the query parameters
    name_filter = request.args.get('name')

    # Retrieve stations with optional filtering by name
    query = Station.query.filter_by(dining_hall_id=id)
    if name_filter:
        query = query.filter(Station.name.like(f"%{name_filter}%"))

    stations = query.all()
    stations_data = [
        {
            "id": station.id,
            "name": station.name,
            "dining_hall_id": station.dining_hall_id,
            "_links": {
                "self": f"/api/v1/dining_halls/{id}/stations/{station.id}",
                "dining_hall": f"/api/v1/dining_halls/{id}"
            }
        } for station in stations
    ]

    # TODO: change this to station_schema.jsonify
    return jsonify(stations_data), 200
    
# POST /api/v1/dining_halls/{id}/stations: Add a new station to a particular dining hall
@dining_halls_bp.route('/dining_halls/<int:id>/stations', methods=['POST'])
def add_station(id):
    """
    Add a new station to a specific dining hall
    ---
    tags:
      - Dining Halls
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the dining hall
        example: 1
      - name: name
        in: body
        required: true
        schema:
          id: Station
          required:
            - dining_hall_id
            - name
          properties:
            name:
              type: string
              description: The name of the new station
              example: "Grill Station"
            dining_hall_id:
              type: integer
              description: The id of the dining hall
              example: 2
    responses:
      201:
        description: Station created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 5
            message:
              type: string
              example: "Station added"
      404:
        description: Dining hall not found
      409:
        description: Station with the same name already exists for this dining hall
    """
    # Verify if the dining hall exists
    dining_hall = DiningHall.query.get(id)
    if not dining_hall:
        return jsonify({"error": "Dining hall not found"}), 404

    # Retrieve station data from request body
    data = request.get_json()
    name = data.get('name')

    # Check if the station with the same name already exists for this dining hall
    existing_station = Station.query.filter_by(name=name, dining_hall_id=id).first()
    if existing_station:
        return jsonify({"error": "Station with the same name already exists for this dining hall"}), 409

    # Create the new station
    new_station = Station(name=name, dining_hall_id=id)
    db.session.add(new_station)
    db.session.commit()

    return jsonify({"id": new_station.id, "message": "Station added"}), 201