from flask import Blueprint, jsonify, request
from models import DiningHall, Station, db
from schemas import DiningHallSchema, StationSchema

# register blueprint and create schemas
dining_halls_bp = Blueprint('dining_halls', __name__)
dining_hall_schema = DiningHallSchema()
dining_halls_schema = DiningHallSchema(many=True)
station_schema = StationSchema()
stations_schema = StationSchema(many=True)

# POST: /api/v1/dining_halls: Create a new dining hall
@dining_halls_bp.route('/dining_halls', methods=['POST'])
def create_dining_hall():
    """
    Create a new dining hall
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
        description: Dining hall created
        schema:
          properties:
            id:
              type: integer
              example: 3
            message:
              type: string
              example: "Dining hall created"
            _links:
              type: object
              properties:
                collection:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dining_halls"
                    method:
                      type: string
                      example: "GET"
                create:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dining_halls"
                    method:
                      type: string
                      example: "POST"
                get_stations:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dining_halls/3/stations"
                    method:
                      type: string
                      example: "GET"
                create_station:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dining_halls/3/stations"
                    method:
                      type: string
                      example: "POST"
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

    return dining_hall_schema.jsonify({"id": new_dining_hall.id, "message": "Dining hall created"}), 201

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
                example: 3
              name:
                type: string
                example: "John Jay"
              _links:
                type: object
                properties:
                  collection:
                    type: object
                    properties:
                      href:
                        type: string
                        example: "/api/v1/dining_halls"
                      method:
                        type: string
                        example: "GET"
                  create:
                    type: object
                    properties:
                      href:
                        type: string
                        example: "/api/v1/dining_halls"
                      method:
                        type: string
                        example: "POST"
                  get_stations:
                    type: object
                    properties:
                      href:
                        type: string
                        example: "/api/v1/dining_halls/3/stations"
                      method:
                        type: string
                        example: "GET"
                  create_station:
                    type: object
                    properties:
                      href:
                        type: string
                        example: "/api/v1/dining_halls/3/stations"
                      method:
                        type: string
                        example: "POST"
    """
    name_filter = request.args.get('name')

    query = db.session.query(DiningHall)
    if name_filter:
        query = query.filter(DiningHall.name.like(f"%{name_filter}%"))

    dining_halls = query.all()
    return dining_halls_schema.jsonify(dining_halls), 200

# DELETE /api/v1/dining_halls/{id}: Delete a dining hall
@dining_halls_bp.route('/dining_halls/<int:id>', methods=['DELETE'])
def delete_dining_hall(id):
    """
    Delete a dining hall by ID
    ---
    tags:
      - Dining Halls
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: The ID of the dining hall to delete
    responses:
      200:
        description: Dining hall deleted
        schema:
          properties:
            id:
              type: integer
              example: 3
            message:
              type: string
              example: "Dining hall deleted"
      404:
        description: Dining hall not found
    """
    dining_hall = DiningHall.query.get(id)
    if not dining_hall:
        return jsonify({"error": "Dining hall not found"}), 404

    db.session.delete(dining_hall)
    db.session.commit()

    return dining_hall_schema.jsonify({"id": dining_hall.id, "message": "Dining hall deleted"}), 200

# GET /api/v1/stations: Retrieve a list of all stations
@dining_halls_bp.route('/stations', methods=['GET'])
def get_all_stations():
    """
    Retrieve a list of all stations
    ---
    tags:
      - Dining Halls
    parameters:
      - name: name
        in: query
        type: string
        description: Filter by station name
        example: "Grill"
    responses:
      200:
        description: A list of all stations
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
                example: 3
              name:
                type: string
                example: "Grill Station"
              dining_hall_id:
                type: integer
                example: 2
              _links:
                type: object
                properties:
                  collection:
                    type: object
                    properties:
                      href:
                        type: string
                        example: "/api/v1/dining_halls/3/stations"
                      method:
                        type: string
                        example: "GET"
                  create:
                    type: object
                    properties:
                      href:
                        type: string
                        example: "/api/v1/dining_halls/3/stations"
                      method:
                        type: string
                        example: "POST"
    """
    name_filter = request.args.get('name')

    query = db.session.query(Station)
    if name_filter:
        query = query.filter(Station.name.like(f"%{name_filter}%"))

    stations = query.all()
    return stations_schema.jsonify(stations), 200

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
                example: 3
              _links:
                type: object
                properties:
                  collection:
                    type: object
                    properties:
                      href:
                        type: string
                        example: "/api/v1/dining_halls/3/stations"
                      method:
                        type: string
                        example: "GET"
                  create:
                    type: object
                    properties:
                      href:
                        type: string
                        example: "/api/v1/dining_halls/3/stations"
                      method:
                        type: string
                        example: "POST"
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
    return stations_schema.jsonify(stations), 200
    
# POST /api/v1/dining_halls/{id}/stations: Create a new station to a particular dining hall
@dining_halls_bp.route('/dining_halls/<int:id>/stations', methods=['POST'])
def create_station(id):
    """
    Create a new station to a specific dining hall
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
            - name
          properties:
            name:
              type: string
              description: The name of the new station
              example: "Grill Station"
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
              example: "Station created"
            _links:
              type: object
              properties:
                collection:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dining_halls/2/stations"
                    method:
                      type: string
                      example: "GET"
                create:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dining_halls/2/stations"
                    method:
                      type: string
                      example: "POST"
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
    return station_schema.jsonify({"id": new_station.id, "dining_hall_id": id, "message": "Station created"}), 201

# DELETE /api/v1/dining_halls/{id}/stations/{station_id}: Delete a station within a specific dining hall
@dining_halls_bp.route('/dining_halls/<int:id>/stations/<int:station_id>', methods=['DELETE'])
def delete_station(id, station_id):
    """
    Delete a station within a specific dining hall
    ---
    tags:
      - Dining Halls
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: ID of the dining hall
      - name: station_id
        in: path
        required: true
        type: integer
        description: ID of the station to delete
    responses:
      200:
        description: Station deleted
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 10
            dining_hall_id:
              type: integer
              example: 3
            message:
              type: string
              example: "Station deleted"
      404:
        description: Dining hall or station not found
    """
    # Verify that the dining hall exists
    dining_hall = DiningHall.query.get(id)
    if not dining_hall:
        return jsonify({"error": "Dining hall not found"}), 404

    # Find the station to delete within the specified dining hall
    station = Station.query.filter_by(id=station_id, dining_hall_id=id).first()
    if not station:
        return jsonify({"error": "Station not found"}), 404

    # Delete the station
    db.session.delete(station)
    db.session.commit()

    return station_schema.jsonify({"id": station_id, "dining_hall_id": id, "message": "Station deleted"}), 200