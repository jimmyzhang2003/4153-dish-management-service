from flask import Flask, request, jsonify
import mysql.connector
from dotenv import load_dotenv
import os

# TODO: table name is currently dishes, adjust it to match the name of the table in the RDS instance
# TODO: GET /featured-dishes: Retrieve a list of the most recently reviewed dishes -> MAYBE add for review service

# Load environment variables
load_dotenv()

app = Flask(__name__)

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
    cursor = db.cursor()
    cursor.execute("DELETE FROM dishes WHERE id=%s", (id, ))
    db.commit()
    cursor.close()
    return jsonify({"message": "Dish deleted"}), 200

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001)