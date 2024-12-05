from flask import Blueprint
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from flask_graphql import GraphQLView
from models import Dish

# register blueprint and create schemas
graphql_bp = Blueprint('graphql', __name__)

class DishType(SQLAlchemyObjectType):
    class Meta:
        model = Dish

class Query(graphene.ObjectType):
    all_dishes = graphene.List(DishType, name=graphene.String())

    def resolve_all_dishes(self, info, name=None):
        # Query all dishes
        query = DishType.get_query(info)

        if name:
            query = query.filter(Dish.name.like(f"%{name}%"))

        return query.all()

# GraphQL endpoint for dishes
@graphql_bp.route('/api/v1/graphql', methods=['GET', 'POST'])
def graphql_view():
    return GraphQLView.as_view('graphql', schema=graphene.Schema(query=Query), graphiql=True)()