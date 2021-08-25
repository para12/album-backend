from graphene import ObjectType, List, Field, String, Mutation, UUID
from graphene_django import DjangoObjectType
# from uuid import UUID

from .models import Album, User
import random

class AlbumType(DjangoObjectType):
    class Meta:
        model = Album
        fields= '__all__'
        # fields= ['id', 'name', 'created_at']


class AllAlbum(ObjectType):
    all_albums = List(AlbumType)
    def resolve_all_albums(root, info):
        return Album.objects.all()


class UserAlbum(ObjectType):
    user_albums = Field(List(AlbumType), username=String()) 
    def resolve_user_albums(root, info, username):
        username_modified = username
        if username == "" :
            users = list(User.objects.all())
            random_user = random.choice(users)
            while random_user.username == 'admin' :
                random_user = random.choice(users)
            username_modified = random_user.username
        return Album.objects.filter(owner__username = username_modified).order_by('-created_at')

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

class DeleteAlbum(Mutation):
    class Arguments:
        id = String()
    album = Field(AlbumType)
    def mutate(root, info, id):
        user = info.context.user
        album = Album.objects.get(id=id)
        original = Album.objects.get(id=id)
        if user.is_authenticated and user == album.owner :
            album.delete()
            return DeleteAlbum(album=original)
        else:
            return None

class ModifyAlbum(Mutation):
    class Arguments:
        id = String()
        name = String()
    album = Field(AlbumType)
    def mutate(root, info, id, name):
        user = info.context.user
        album = Album.objects.get(id=id)
        if user.is_authenticated and user == album.owner :
            setattr(album, 'name', name)
            album.save()
            return ModifyAlbum(album=album)
        else:
            return None

class AlbumQuery(AllAlbum, UserAlbum):
    pass


class AlbumMutation(ObjectType):
    create_album = CreateAlbum.Field()
    delete_album = DeleteAlbum.Field()
    modify_album = ModifyAlbum.Field()