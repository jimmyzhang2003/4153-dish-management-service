from flask import Blueprint, jsonify, request
from models import DiningHall, db
from schemas import DiningHallSchema

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
              example: "Main Dining Hall"
    responses:
      201:
        description: Dining hall added
        schema:
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: "Main Dining Hall"
      400:
        description: Name is required
    """
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({"error": "Name is required"}), 400

    new_dining_hall = DiningHall(name=name)
    db.session.add(new_dining_hall)
    db.session.commit()

    return dining_hall_schema.jsonify(new_dining_hall), 201

# GET /api/v1/dining_halls/{id}: Retrieve dining hall details
@dining_halls_bp.route('/dining_halls/<int:id>', methods=['GET'])
def get_dining_hall(id):
    """
    Retrieve detailed information about a specific dining hall
    ---
    tags:
      - Dining Halls
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: ID of the dining hall
        example: 1
    responses:
      200:
        description: A dining hall
        schema:
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: "Main Hall"
            _links:
              type: object
              properties:
                collection:
                  type: string
                  example: "/api/v1/dining_halls"
                self:
                  type: string
                  example: "/api/v1/dining_halls/{id}"
                update:
                  type: string
                  example: "/api/v1/dining_halls/{id}"
      404:
        description: Dining hall not found
    """
    dining_hall = db.session.query(DiningHall).get(id)
    if not dining_hall:
        return jsonify({"error": "Dining hall not found"}), 404
    return dining_hall_schema.jsonify(dining_hall), 200



# GET /dining_halls/id/stations
# POST