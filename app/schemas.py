from flask_marshmallow import Marshmallow
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
    
    # Adding HATEOAS links
    _links = ma.Hyperlinks({
        "self": ma.URLFor("dishes.get_dish", values=dict(id="<id>")),
        "update": ma.URLFor("dishes.update_dish", values=dict(id="<id>")),
        "delete": ma.URLFor("dishes.delete_dish", values=dict(id="<id>")),
        "collection": ma.URLFor("dishes.get_dishes")
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