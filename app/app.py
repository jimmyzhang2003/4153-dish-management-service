import logging
from datetime import datetime
from flask import Flask, request, redirect, jsonify, g
from flask_cors import CORS
from flasgger import Swagger
from flask_marshmallow import Marshmallow
from config import db, config_db
from model import Dish

# TODO: table name is currently dishes, adjust it to match the name of the table in the RDS instance
# TODO: GET /featured-dishes: Retrieve a list of the most recently reviewed dishes -> MAYBE add for review service

# Create Flask app
app = Flask(__name__)
CORS(app)

# Connect to MySQL database
config_db(app)

# Create Marshmallow instance for HATEOAS
ma = Marshmallow(app)

# Create Marshmallow output schema
class DishSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Dish

    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    category = ma.auto_field()
    dietary_info = ma.auto_field()
    
    # Adding HATEOAS links
    _links = ma.Hyperlinks({
        "self": ma.URLFor("get_dish", values=dict(id="<id>")),
        "update": ma.URLFor("update_dish", values=dict(id="<id>")),
        "delete": ma.URLFor("delete_dish", values=dict(id="<id>")),
        "collection": ma.URLFor("get_dishes")
    })

dish_schema = DishSchema()
dishes_schema = DishSchema(many=True)

# Create Swagger documentation
template = {
  "swagger": "2.0",
  "info": {
    "title": "Dish Management Service",
    "version": "0.0.1"
  },
  "host": "localhost:5001", 
  "schemes": [
    "http",
  ],
}
swagger = Swagger(app, template=template)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Middleware logging before each request
@app.before_request
def before_request_logging():
    g.start_time = datetime.now()
    logger.info(f"Incoming {request.method} request to {request.path} with data: {request.args.to_dict()}")

# Middleware logging after each request
@app.after_request
def after_request_logging(response):
    duration = datetime.now() - g.start_time
    logger.info(f"Completed {request.method} request to {request.path} in {duration.total_seconds()} seconds with status code {response.status_code}")
    return response

# -----------------------------------------------------------

# GET /: Redirect to Swagger page
@app.route('/', methods=['GET'])
def root():
    return redirect("/apidocs", code=302)

# GET /api/v1/: Redirect to Swagger page
@app.route('/api/v1/', methods=['GET'])
def api_root():
    return redirect("/apidocs", code=302)

# POST /api/v1/dishes: Add a new dish
@app.route('/api/v1/dishes', methods=['POST'])
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
    new_dish_data = request.json
    new_dish = Dish(
        name=new_dish_data['name'],
        description=new_dish_data.get('description'),
        category=new_dish_data.get('category'),
        dietary_info=new_dish_data.get('dietary_info')
    )
    db.session.add(new_dish)
    db.session.commit()
    return jsonify({"id": new_dish.id, "message": "Dish added"}), 201

# GET /api/v1/dishes: Retrieve a list of all dishes
@app.route('/api/v1/dishes', methods=['GET'])
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
    """
    name_filter = request.args.get('name')
    category_filter = request.args.get('category')

    query = db.session.query(Dish)
    if name_filter:
        query = query.filter(Dish.name.like(f"%{name_filter}%"))
    if category_filter:
        query = query.filter(Dish.category == category_filter)
    
    dishes = query.all()
    return dishes_schema.jsonify(dishes), 200

# GET /api/v1/dishes/{id}: Retrieve dish details
@app.route('/api/v1/dishes/<int:id>', methods=['GET'])
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
      404:
        description: Dish not found
    """
    dish = db.session.query(Dish).get(id)
    if not dish:
        return jsonify({"error": "Dish not found"}), 404
    return dish_schema.jsonify(dish), 200

# PUT /api/v1/dishes/{id}: Update dish details
@app.route('/api/v1/dishes/<int:id>', methods=['PUT'])
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
    if 'category' in updated_data:
        dish.category = updated_data['category']
    if 'dietary_info' in updated_data:
        dish.dietary_info = updated_data['dietary_info']
    db.session.commit()
    return jsonify({"message": "Dish updated"}), 200

# DELETE /api/v1/dishes/{id}: Delete a dish
@app.route('/api/v1/dishes/<int:id>', methods=['DELETE'])
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

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001)