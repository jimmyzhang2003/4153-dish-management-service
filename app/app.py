from flask import Flask, request, redirect, jsonify, url_for
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

# GET /: Redirect to Swagger page
@app.route('/', methods=['GET'])
def root():
    return redirect("/apidocs", code = 302)

# GET /api/v1/: Redirect to Swagger page
@app.route('/api/v1/', methods=['GET'])
def api_root():
    return redirect("/apidocs", code = 302)

# POST /api/v1/dishes: Add a new dish
@app.route('/api/v1/dishes', methods=['POST'])
def add_dish():
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

# GET /api/v1/dishes: Retrieve a list of all dishes (with filtering capabilities)
@app.route('/api/v1/dishes', methods=['GET'])
def get_dishes():
    name_filter = request.args.get('name')
    category_filter = request.args.get('category')

    query = db.session.query(Dish)
    
    if name_filter:
        query = query.filter(Dish.name.like(f"%{name_filter}%"))
    
    if category_filter:
        query = query.filter(Dish.category == category_filter)
    
    dishes = query.all()
    return dishes_schema.jsonify(dishes), 200

# GET /api/v1/dishes/{id}: Retrieve detailed information about a specific dish
@app.route('/api/v1/dishes/<int:id>', methods=['GET'])
def get_dish(id):
    dish = db.session.query(Dish).get(id)
    if not dish:
        return jsonify({"error": "Dish not found"}), 404

    return dish_schema.jsonify(dish), 200

# PUT /api/v1/dishes/{id}: Update details of an existing dish
@app.route('/api/v1/dishes/<int:id>', methods=['PUT'])
def update_dish(id):
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
    dish = db.session.query(Dish).get(id)
    if not dish:
        return jsonify({"error": "Dish not found"}), 404

    db.session.delete(dish)
    db.session.commit()
    return jsonify({"message": "Dish deleted"}), 200

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001)