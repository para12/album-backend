from graphene import ObjectType, List, Schema
from graphene_django import DjangoObjectType
from .auth import AuthQuery, AuthMutation

from .models import User, Album

class AlbumType(DjangoObjectType):
    class Meta:
        model = Album
        fields= '__all__'



class Query(AuthQuery, ObjectType):
    all_albums = List(AlbumType)
    def resolve_all_albums(root, info):
        return Album.objects.all()
    pass

class Mutation(AuthMutation, ObjectType):
    pass

schema = Schema(query=Query, mutation=Mutation)