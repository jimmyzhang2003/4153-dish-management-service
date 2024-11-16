from flask import Blueprint, jsonify, request
from models import Dish, DiningHall, Station, db
from schemas import DishSchema

# register blueprint and create schemas
dishes_bp = Blueprint('dishes', __name__)
dish_schema = DishSchema()
dishes_schema = DishSchema(many=True)

# POST /api/v1/dishes: Create a new dish
@dishes_bp.route('/dishes', methods=['POST'])
def create_dish():
    """
    Create a new dish
    ---
    tags:
      - Dishes
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Dish
          required:
            - name
            - dining_hall_id
            - station_id
          properties:
            name:
              type: string
              description: The name of the dish
              example: "Spaghetti Carbonara"
            description:
              type: string
              description: Description of the dish
              example: "Classic Italian pasta with egg, cheese, pancetta, and pepper."
            dining_hall_id:
              type: integer
              description: The id of the dining hall
              example: 2
            station_id:
              type: integer
              description: The id of the station
              example: 10
    responses:
      201:
        description: Dish created
        schema:
          properties:
            id:
              type: integer
              example: 3
            message:
              type: string
              example: "Dish created"
            _links:
              type: object
              properties:
                collection:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dishes"
                    method:
                      type: string
                      example: "GET"
                create:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dishes"
                    method:
                      type: string
                      example: "POST"
                delete:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dishes/3"
                    method:
                      type: string
                      example: "DELETE"
                self:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dishes/3"
                    method:
                      type: string
                      example: "GET"
                update:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dishes/3"
                    method:
                      type: string
                      example: "PUT"
      400:
        description: Invalid input
      409:
        description: Dish with the same name already exists for this dining hall and station
    """
    data = request.json
    name = data.get('name')
    dining_hall_id = data.get('dining_hall_id')
    station_id = data.get('station_id')

    # Validate dining hall and station
    dining_hall = DiningHall.query.get(dining_hall_id)
    if not dining_hall:
        return jsonify({"error": "Invalid dining_hall_id"}), 400

    station = Station.query.get(station_id)
    if not station or station.dining_hall_id != dining_hall_id:
        return jsonify({"error": "Invalid station_id for this dining hall"}), 400

    # Check if a dish with the same name already exists for this dining hall and station
    existing_dish = Dish.query.filter_by(name=name, dining_hall_id=dining_hall_id, station_id=station_id).first()
    if existing_dish:
        return jsonify({"error": "Dish with the same name already exists for this dining hall and station"}), 409

    # Create the new dish
    new_dish = Dish(**data)
    db.session.add(new_dish)
    db.session.commit()
    
    return dish_schema.jsonify({"id": new_dish.id, "message": "Dish created"}), 201

# GET /api/v1/dishes: Retrieve a list of all dishes
@dishes_bp.route('/dishes', methods=['GET'])
def get_dishes():
    """
    Retrieve a list of all dishes
    ---
    tags:
      - Dishes
    parameters:
      - name: name
        in: query
        type: string
        description: Filter by name
        example: "Spaghetti"
      - name: description
        in: query
        type: string
        description: Filter by description
        example: "pasta"
      - name: dining_hall_id
        in: query
        type: integer
        description: Filter by dining_hall_id
        example: 2
      - name: station_id
        in: query
        type: string
        description: Filter by station_id
        example: 10
      - name: limit
        in: query
        type: integer
        description: Limit on the number of dishes returned (default 10)
        example: 5
    responses:
      200:
        description: A list of dishes
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
                example: 3
              name:
                type: string
                example: "Spaghetti Carbonara"
              description:
                type: string
                example: "Classic Italian pasta with egg, cheese, pancetta, and pepper."
              dining_hall_id:
                type: integer
                example: 2
              station_id:
                type: integer
                example: 10
              _links:
                type: object
                properties:
                  collection:
                    type: object
                    properties:
                      href:
                        type: string
                        example: "/api/v1/dishes"
                      method:
                        type: string
                        example: "GET"
                  create:
                    type: object
                    properties:
                      href:
                        type: string
                        example: "/api/v1/dishes"
                      method:
                        type: string
                        example: "POST"
                  delete:
                    type: object
                    properties:
                      href:
                        type: string
                        example: "/api/v1/dishes/3"
                      method:
                        type: string
                        example: "DELETE"
                  self:
                    type: object
                    properties:
                      href:
                        type: string
                        example: "/api/v1/dishes/3"
                      method:
                        type: string
                        example: "GET"
                  update:
                    type: object
                    properties:
                      href:
                        type: string
                        example: "/api/v1/dishes/3"
                      method:
                        type: string
                        example: "PUT"
    """
    name_filter = request.args.get('name')
    description_filter = request.args.get('description')
    dining_hall_filter = request.args.get('dining_hall_id')
    station_filter = request.args.get('station_id')

    # set limit to 10 if not specified
    limit = request.args.get('limit', default=10, type=int)

    query = db.session.query(Dish)
    if name_filter:
        query = query.filter(Dish.name.like(f"%{name_filter}%"))
    if description_filter:
        query = query.filter(Dish.description.like(f"%{description_filter}%"))  
    if dining_hall_filter:
        query = query.filter(Dish.dining_hall_id == dining_hall_filter)
    if station_filter:
        query = query.filter(Dish.station_id == station_filter)
    
    dishes = query.limit(limit).all()
    return dishes_schema.jsonify(dishes), 200

# GET /api/v1/dishes/{id}: Retrieve dish details
@dishes_bp.route('/dishes/<int:id>', methods=['GET'])
def get_dish(id):
    """
    Retrieve detailed information about a specific dish
    ---
    tags:
      - Dishes
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: ID of the dish
        example: 1
    responses:
      200:
        description: A dish
        schema:
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: "Spaghetti Carbonara"
            description:
              type: string
              example: "Classic Italian pasta with egg, cheese, pancetta, and pepper."
            dining_hall_id:
              type: integer
              example: 2
            station_id:
              type: integer
              example: 10
            _links:
              type: object
              properties:
                collection:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dishes"
                    method:
                      type: string
                      example: "GET"
                create:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dishes"
                    method:
                      type: string
                      example: "POST"
                delete:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dishes/3"
                    method:
                      type: string
                      example: "DELETE"
                self:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dishes/3"
                    method:
                      type: string
                      example: "GET"
                update:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dishes/3"
                    method:
                      type: string
                      example: "PUT"
      404:
        description: Dish not found
    """
    dish = db.session.query(Dish).get(id)
    if not dish:
        return jsonify({"error": "Dish not found"}), 404
    return dish_schema.jsonify(dish), 200

# PUT /api/v1/dishes/{id}: Update dish details
@dishes_bp.route('/dishes/<int:id>', methods=['PUT'])
def update_dish(id):
    """
    Update details of an existing dish
    ---
    tags:
      - Dishes
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: ID of the dish
        example: 1
      - name: body
        in: body
        required: true
        schema:
          properties:
            name:
              type: string
              example: "Spaghetti Bolognese"
            description:
              type: string
              example: "Pasta with ground beef in a tomato sauce."
            dining_hall_id:
              type: integer
              description: The id of the dining hall
              example: 2
            station_id:
              type: integer
              description: The id of the station
              example: 10
    responses:
      200:
        description: Dish updated
        schema:
          properties:
            id:
              type: integer
              example: 3
            message:
              type: string
              example: "Dish updated"
            _links:
              type: object
              properties:
                collection:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dishes"
                    method:
                      type: string
                      example: "GET"
                create:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dishes"
                    method:
                      type: string
                      example: "POST"
                delete:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dishes/3"
                    method:
                      type: string
                      example: "DELETE"
                self:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dishes/3"
                    method:
                      type: string
                      example: "GET"
                update:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dishes/3"
                    method:
                      type: string
                      example: "PUT"
      404:
        description: Dish not found
    """
    updated_data = request.json
    dish = db.session.query(Dish).get(id)
    if not dish:
        return jsonify({"error": "Dish not found"}), 404
    if 'name' in updated_data:
        dish.name = updated_data['name']
    if 'description' in updated_data:
        dish.description = updated_data['description']
    if 'station' in updated_data:
        dish.station = updated_data['station']
    if 'dietary_info' in updated_data:
        dish.dietary_info = updated_data['dietary_info']
    if 'dining_hall_id' in updated_data:
        dish.dining_hall_id = updated_data['dining_hall_id']
    db.session.commit()
    return dish_schema.jsonify({"id": dish.id, "message": "Dish updated"}), 200

# DELETE /api/v1/dishes/{id}: Delete a dish
@dishes_bp.route('/dishes/<int:id>', methods=['DELETE'])
def delete_dish(id):
    """
    Delete a dish
    ---
    tags:
      - Dishes
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: ID of the dish
        example: 1
    responses:
      200:
        description: Dish deleted
        schema:
          properties:
            id:
              type: integer
              example: 3
            message:
              type: string
              example: "Dish deleted"
            _links:
              type: object
              properties:
                collection:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dishes"
                    method:
                      type: string
                      example: "GET"
                create:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dishes"
                    method:
                      type: string
                      example: "POST"
                delete:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dishes/3"
                    method:
                      type: string
                      example: "DELETE"
                self:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dishes/3"
                    method:
                      type: string
                      example: "GET"
                update:
                  type: object
                  properties:
                    href:
                      type: string
                      example: "/api/v1/dishes/3"
                    method:
                      type: string
                      example: "PUT"
      404:
        description: Dish not found
    """
    dish = db.session.query(Dish).get(id)
    if not dish:
        return jsonify({"error": "Dish not found"}), 404
    db.session.delete(dish)
    db.session.commit()
    return dish_schema.jsonify({"id": dish.id, "message": "Dish deleted"}), 200