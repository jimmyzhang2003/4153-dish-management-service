from flask import request
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
            "rel": "self",
            "href": ma.URLFor("dishes.get_dish", values=dict(id="<id>")),
            "method": "GET"
        },
        "update": {
            "rel": "update",
            "href": ma.URLFor("dishes.update_dish", values=dict(id="<id>")),
            "method": "PUT"
        },
        "delete": {
            "rel": "delete",
            "href": ma.URLFor("dishes.delete_dish", values=dict(id="<id>")),
            "method": "DELETE"
        },
        "collection": {
            "rel": "collection",
            "href": ma.URLFor("dishes.get_dishes"),
            "method": "GET"
        },
        "create": {
            "rel": "create",
            "href": ma.URLFor("dishes.add_dish"),
            "method": "POST"
        }
    })

class DiningHallSchema(ma.SQLAlchemySchema):
    class Meta:
        model = DiningHall

    id = ma.auto_field()
    name = ma.auto_field()

dining_hall_schema = DiningHallSchema()
dining_halls_schema = DiningHallSchema(many=True)

class StationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Station
    
    id = ma.auto_field()
    name = ma.auto_field()
    dining_hall_id = ma.auto_field()