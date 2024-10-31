from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from flask_marshmallow import Marshmallow
from config import config_db
from middleware import before_request_logging, after_request_logging

from routes.dish_routes import dishes_bp
from routes.dining_hall_routes import dining_halls_bp
from routes.station_routes import stations_bp
from routes.redirect_routes import redirect_bp

# TODO: table name is currently dishes, adjust it to match the name of the table in the RDS instance
# TODO: GET /featured-dishes: Retrieve a list of the most recently reviewed dishes -> MAYBE add for review service

'''
TODO:
- add logic checks (e.g., if dining hall doesn't exist, create new one)
- don't create new if already exists (all the fields match)
- refer to culpa write a review
'''


# Create Flask app
app = Flask(__name__)
CORS(app)

# Connect to MySQL database
config_db(app)

# Create Marshmallow instance for HATEOAS
ma = Marshmallow(app)

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

# Configure middleware logging
app.before_request(before_request_logging)
app.after_request(after_request_logging)

# Register blueprints
app.register_blueprint(dishes_bp, url_prefix="/api/v1")
app.register_blueprint(dining_halls_bp, url_prefix="/api/v1")
app.register_blueprint(stations_bp, url_prefix="/api/v1")
app.register_blueprint(redirect_bp)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001)