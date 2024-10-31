from flask import Blueprint, jsonify, request
from models import Dish, DiningHall, db
from schemas import DishSchema

# register blueprint and create schemas
dishes_bp = Blueprint('dishes', __name__)
dish_schema = DishSchema()
dishes_schema = DishSchema(many=True)

# POST /api/v1/dishes: Add a new dish
@dishes_bp.route('/dishes', methods=['POST'])
def add_dish():
    """
    Add a new dish
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
          properties:
            name:
              type: string
              description: The name of the dish
              example: "Spaghetti Carbonara"
            description:
              type: string
              description: Description of the dish
              example: "Classic Italian pasta with egg, cheese, pancetta, and pepper."
            category:
              type: string
              description: The category of the dish
              example: "Pasta"
            dietary_info:
              type: string
              description: Dietary information
              example: "Contains dairy and gluten"
    responses:
      201:
        description: Dish added
        schema:
          properties:
            id:
              type: integer
              example: 1
            message:
              type: string
              example: "Dish added"
      400:
        description: Invalid input
    """
    data = request.json
    dining_hall_id = data.get('dining_hall_id')

    # if the dining_hall_id does not exist
    dining_hall = DiningHall.query.filter_by(id=dining_hall_id).first()
    if not dining_hall:
        return jsonify({"error": "Invalid dining_hall_id"}), 400
    
    new_dish = Dish(**data)
    db.session.add(new_dish)
    db.session.commit()
    return jsonify({"id": new_dish.id, "message": "Dish added"}), 201

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
      - name: category
        in: query
        type: string
        description: Filter by category
        example: "Pasta"
    responses:
      200:
        description: A list of dishes
        schema:
          type: array
          items:
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
              category:
                type: string
                example: "Pasta"
              dietary_info:
                type: string
                example: "Contains dairy and gluten"
              _links:
                type: object
                properties:
                  collection:
                    type: string
                    example: "/api/v1/dishes"
                  self:
                    type: string
                    example: "/api/v1/dishes/{id}"
                  delete:
                    type: string
                    example: "/api/v1/dishes/{id}"
                  update:
                    type: string
                    example: "/api/v1/dishes/{id}"
    """
    name_filter = request.args.get('name')
    description_filter = request.args.get('description')
    dining_hall_filter = request.args.get('dining_hall_id')
    station_filter = request.args.get('station_id')

    query = db.session.query(Dish)
    if name_filter:
        query = query.filter(Dish.name.like(f"%{name_filter}%"))
    if description_filter:
        query = query.filter(Dish.description.like(f"%{description_filter}%"))  
    if dining_hall_filter:
        query = query.filter(Dish.dining_hall_id == dining_hall_filter)
    if station_filter:
        query = query.filter(Dish.station_id == station_filter)
    
    dishes = query.all()
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
            category:
              type: string
              example: "Pasta"
            dietary_info:
              type: string
              example: "Contains dairy and gluten"
            _links:
              type: object
              properties:
                collection:
                  type: string
                  example: "/api/v1/dishes"
                self:
                  type: string
                  example: "/api/v1/dishes/{id}"
                delete:
                  type: string
                  example: "/api/v1/dishes/{id}"
                update:
                  type: string
                  example: "/api/v1/dishes/{id}"
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
            category:
              type: string
              example: "Pasta"
            dietary_info:
              type: string
              example: "Contains gluten"
    responses:
      200:
        description: Dish updated
        schema:
          properties:
            message:
              type: string
              example: "Dish updated"
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
    return jsonify({"message": "Dish updated"}), 200

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
            message:
              type: string
              example: "Dish deleted"
      404:
        description: Dish not found
    """
    dish = db.session.query(Dish).get(id)
    if not dish:
        return jsonify({"error": "Dish not found"}), 404
    db.session.delete(dish)
    db.session.commit()
    return jsonify({"message": "Dish deleted"}), 200