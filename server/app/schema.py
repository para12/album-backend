from graphene import ObjectType, List, Schema
from graphene_django import DjangoObjectType
from .auth import AuthQuery, AuthMutation

from .models import User

class Query(AuthQuery, ObjectType):
    pass

class Mutation(AuthMutation, ObjectType):
    pass

schema = Schema(query=Query, mutation=Mutation)