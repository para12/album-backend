from graphene import ObjectType, List, Schema
from graphene_django import DjangoObjectType
from .auth import AuthQuery, AuthMutation
from .album import AlbumQuery, AlbumMutation
from .photo import PhotoQuery, PhotoMutation

from .models import User, Album

class Query(AuthQuery, AlbumQuery, PhotoQuery, ObjectType):
    pass

class Mutation(AuthMutation, AlbumMutation, PhotoMutation, ObjectType):
    pass

schema = Schema(query=Query, mutation=Mutation)