from flask_marshmallow import Marshmallow
from marshmallow import fields
from models import Dish, DiningHall, Station

ma = Marshmallow()

class DishSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Dish

    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    station_id = ma.auto_field()
    dining_hall_id = ma.auto_field()

    # message field for non-GET requests
    message = fields.String(allow_none=True)
    
    # HATEOAS links
    _links = ma.Hyperlinks({
        "self": {
            "href": ma.URLFor("dishes.get_dish", values=dict(id="<id>")),
            "method": "GET"
        },
        "update": {
            "href": ma.URLFor("dishes.update_dish", values=dict(id="<id>")),
            "method": "PUT"
        },
        "delete": {
            "href": ma.URLFor("dishes.delete_dish", values=dict(id="<id>")),
            "method": "DELETE"
        },
        "collection": {
            "href": ma.URLFor("dishes.get_dishes"),
            "method": "GET"
        },
        "create": {
            "href": ma.URLFor("dishes.create_dish"),
            "method": "POST"
        }
    })

class DiningHallSchema(ma.SQLAlchemySchema):
    class Meta:
        model = DiningHall

    id = ma.auto_field()
    name = ma.auto_field()

    # message field for non-GET requests
    message = fields.String(allow_none=True)

    # HATEOAS links
    _links = ma.Hyperlinks({
        "collection": {
            "href": ma.URLFor("dining_halls.get_dining_halls"),
            "method": "GET"
        },
        "create": {
            "href": ma.URLFor("dining_halls.create_dining_hall"),
            "method": "POST"
        },
        "get_stations": {
            "href": ma.URLFor("dining_halls.get_stations", values=dict(id="<id>")),
            "method": "GET"
        },
        "create_station": {
            "href": ma.URLFor("dining_halls.create_station", values=dict(id="<id>")),
            "method": "POST"
        }
    })

dining_hall_schema = DiningHallSchema()
dining_halls_schema = DiningHallSchema(many=True)

class StationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Station
    
    id = ma.auto_field()
    name = ma.auto_field()
    dining_hall_id = ma.auto_field()

    # message field for non-GET requests
    message = fields.String(allow_none=True)

    # HATEOAS links
    _links = ma.Hyperlinks({
        "full_collection": {
            "href": ma.URLFor("dining_halls.get_all_stations"),
            "method": "GET"
        },
        "collection": {
            "href": ma.URLFor("dining_halls.get_stations", values=dict(id="<dining_hall_id>")),
            "method": "GET"
        },
        "create": {
            "href": ma.URLFor("dining_halls.create_station", values=dict(id="<dining_hall_id>")),
            "method": "POST"
        }
    })