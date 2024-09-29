from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for dishes (this would typically be a database)
dishes = []
next_id = 1

# Dish structure example:
# {
#     "id": 1,
#     "name": "Pizza",
#     "description": "Cheese and tomato pizza",
#     "category": "Main Course",
#     "dietary_info": "Vegetarian"
# }

# POST /dishes: Add a new dish
@app.route('/dishes', methods=['POST'])
def add_dish():
    global next_id
    new_dish = request.json
    new_dish['id'] = next_id
    next_id += 1
    dishes.append(new_dish)
    return jsonify(new_dish), 201

# GET /dishes: Retrieve a list of all dishes (with filtering capabilities)
@app.route('/dishes', methods=['GET'])
def get_dishes():
    name_filter = request.args.get('name')
    category_filter = request.args.get('category')
    
    filtered_dishes = [dish for dish in dishes if
                       (not name_filter or name_filter.lower() in dish['name'].lower()) and
                       (not category_filter or category_filter.lower() == dish['category'].lower())]
    
    return jsonify(filtered_dishes), 200

# GET /dishes/{id}: Retrieve detailed information about a specific dish
@app.route('/dishes/<int:id>', methods=['GET'])
def get_dish(id):
    dish = next((dish for dish in dishes if dish['id'] == id), None)
    if dish is None:
        return jsonify({"error": "Dish not found"}), 404
    return jsonify(dish), 200

# PUT /dishes/{id}: Update details of an existing dish
@app.route('/dishes/<int:id>', methods=['PUT'])
def update_dish(id):
    dish = next((dish for dish in dishes if dish['id'] == id), None)
    if dish is None:
        return jsonify({"error": "Dish not found"}), 404
    
    updated_data = request.json
    dish.update(updated_data)
    return jsonify(dish), 200

# DELETE /dishes/{id}: Delete a dish
@app.route('/dishes/<int:id>', methods=['DELETE'])
def delete_dish(id):
    global dishes
    dishes = [dish for dish in dishes if dish['id'] != id]
    return jsonify({"message": "Dish deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
