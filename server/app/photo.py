from graphene import ObjectType, List, Field, String, Mutation
from graphene_django import DjangoObjectType

from .models import Album

class AlbumType(DjangoObjectType):
    class Meta:
        model = Album
        fields= '__all__'


class AllAlbum(ObjectType):
    all_albums = List(AlbumType)
    def resolve_all_albums(root, info):
        return Album.objects.all()


class CreateAlbum(Mutation):
    class Arguments:
        name = String()
    album = Field(AlbumType)
    def mutate(root, info, name):
        if info.context.user.is_authenticated:
            album = Album.objects.create(name=name, owner=info.context.user)
            album.save()
            return CreateAlbum(album=album)
        else:
            return None

class AlbumQuery(AllAlbum):
    pass


class AlbumMutation(ObjectType):
    create_album = CreateAlbum.Field()