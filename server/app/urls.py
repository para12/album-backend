from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from .schema import schema
# from graphql_jwt.decorators import jwt_cookie

urlpatterns = [
    # path('graphql', csrf_exempt(jwt_cookie(GraphQLView.as_view(graphiql=True, schema=schema)))),
    path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    # path('graphql', GraphQLView.as_view(graphiql=True, schema=schema)),
]