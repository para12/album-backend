from graphene import ObjectType, List, Schema
from graphene_django import DjangoObjectType
from .auth import AuthQuery, AuthMutation
from .album import AlbumQuery, AlbumMutation

from .models import User, Album

class Query(AuthQuery, AlbumQuery, ObjectType):
    pass

class Mutation(AuthMutation, AlbumMutation, ObjectType):
    pass

schema = Schema(query=Query, mutation=Mutation)