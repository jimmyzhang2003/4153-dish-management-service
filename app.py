from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger
import mysql.connector
from dotenv import load_dotenv
import os

# TODO: table name is currently dishes, adjust it to match the name of the table in the RDS instance
# TODO: GET /featured-dishes: Retrieve a list of the most recently reviewed dishes -> MAYBE add for review service

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app)

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

# Connect to MySQL database
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# POST /dishes: Add a new dish
@app.route('/dishes', methods=['POST'])
def add_dish():
    """
    Add a new dish.
    ---
    tags:
      - Dishes
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
            - description
            - category
            - dietary_info
          properties:
            name:
              type: string
              description: The name of the dish
            description:
              type: string
              description: A description of the dish
            category:
              type: string
              description: The category of the dish (e.g., appetizer, main course)
            dietary_info:
              type: string
              description: Dietary information (e.g., vegan, gluten-free)
    responses:
      201:
        description: Dish successfully created
        schema:
          type: object
          properties:
            id:
              type: integer
              description: The ID of the new dish
            name:
              type: string
            description:
              type: string
            category:
              type: string
            dietary_info:
              type: string
    """
    new_dish = request.json
    cursor = db.cursor()
    cursor.execute("INSERT INTO dishes (name, description, category, dietary_info) VALUES (%s, %s, %s, %s)", 
                   (new_dish['name'], new_dish['description'], new_dish['category'], new_dish['dietary_info']))
    db.commit()
    new_dish['id'] = cursor.lastrowid
    cursor.close()
    return jsonify(new_dish), 201

# GET /dishes: Retrieve a list of all dishes (with filtering capabilities)
@app.route('/dishes', methods=['GET'])
def get_dishes():
    """
    Retrieve a list of all dishes.
    ---
    tags:
      - Dishes
    parameters:
      - in: query
        name: name
        type: string
        required: false
        description: Filter dishes by name (partial matches allowed)
      - in: query
        name: category
        type: string
        required: false
        description: Filter dishes by category
    responses:
      200:
        description: List of filtered dishes
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              description:
                type: string
              category:
                type: string
              dietary_info:
                type: string
    """
    name_filter = request.args.get('name')
    category_filter = request.args.get('category')

    query = "SELECT * FROM dishes WHERE 1=1"
    params = []
    
    if name_filter:
        query += " AND name LIKE %s"
        params.append(f"%{name_filter}%")
    
    if category_filter:
        query += " AND category = %s"
        params.append(category_filter)

    cursor = db.cursor(dictionary=True)
    cursor.execute(query, params)
    filtered_dishes = cursor.fetchall()
    cursor.close()
    return jsonify(filtered_dishes), 200

# GET /dishes/{id}: Retrieve detailed information about a specific dish
@app.route('/dishes/<int:id>', methods=['GET'])
def get_dish(id):
    """
    Retrieve detailed information about a specific dish.
    ---
    tags:
      - Dishes
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: The ID of the dish
    responses:
      200:
        description: Details of the specified dish
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            description:
              type: string
            category:
              type: string
            dietary_info:
              type: string
      404:
        description: Dish not found
    """
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM dishes WHERE id = %s", (id, ))
    dish = cursor.fetchone()
    cursor.close()
    if dish is None:
        return jsonify({"error": "Dish not found"}), 404
    return jsonify(dish), 200

# PUT /dishes/{id}: Update details of an existing dish
@app.route('/dishes/<int:id>', methods=['PUT'])
def update_dish(id):
    """
    Update details of an existing dish.
    ---
    tags:
      - Dishes
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: The ID of the dish
      - in: body
        name: body
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
            category:
              type: string
            dietary_info:
              type: string
    responses:
      200:
        description: Dish updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: Dish updated
      400:
        description: No fields provided to update
    """
    updated_data = request.json
    cursor = db.cursor()

    fields = []
    values = []
    
    if 'name' in updated_data:
        fields.append("name = %s")
        values.append(updated_data['name'])
    
    if 'description' in updated_data:
        fields.append("description = %s")
        values.append(updated_data['description'])
    
    if 'category' in updated_data:
        fields.append("category = %s")
        values.append(updated_data['category'])
    
    if 'dietary_info' in updated_data:
        fields.append("dietary_info = %s")
        values.append(updated_data['dietary_info'])

    # If there are no fields to update, return an error response
    if not fields:
        return jsonify({"message": "No fields provided to update"}), 400

    # Add the dish ID to the list of values
    values.append(id)
    
    query = f"UPDATE dishes SET {', '.join(fields)} WHERE id = %s"

    cursor.execute(query, values)
    db.commit()
    cursor.close()
    return jsonify({"message": "Dish updated"}), 200

# DELETE /dishes/{id}: Delete a dish
@app.route('/dishes/<int:id>', methods=['DELETE'])
def delete_dish(id):
    """
    Delete a dish.
    ---
    tags:
      - Dishes
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: The ID of the dish
    responses:
      200:
        description: Dish deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: Dish deleted
    """
    cursor = db.cursor()
    cursor.execute("DELETE FROM dishes WHERE id=%s", (id, ))
    db.commit()
    cursor.close()
    return jsonify({"message": "Dish deleted"}), 200

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001)