from graphene import ObjectType, List, Field, String, Mutation, UUID
from graphene_django import DjangoObjectType
# from uuid import UUID

from .models import Album, User
import random
import boto3
import logging
import os
from botocore.exceptions import ClientError
from botocore.config import Config
import json
import uuid


def create_presigned_post(object_name, fields=None, conditions=None, expiration=10):

    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3', aws_access_key_id=os.environ.get("S3_ACS_KEY"), aws_secret_access_key=os.environ.get(
        "S3_ACS_SEC"), config=Config(signature_version='s3v4'), region_name=os.environ.get("S3_REGION"))
    try:
        response = s3_client.generate_presigned_post(os.environ.get("S3_BUCKET_NAME"), 
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
        # response = s3_client.generate_presigned_post(os.environ.get("S3_BUCKET_NAME"), 
        #                                              object_name,
        #                                              Fields={"ACL": "public-read"},
        #                                              Conditions=[{"ACL": "public-read"}],
        #                                              ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response


class AlbumType(DjangoObjectType):
    class Meta:
        model = Album
        fields = '__all__'
        # fields= ['id', 'name', 'created_at']


class AllAlbum(ObjectType):
    all_albums = List(AlbumType)

    def resolve_all_albums(root, info):
        return Album.objects.all()


class UserAlbum(ObjectType):
    user_albums = Field(List(AlbumType), username=String())

    def resolve_user_albums(root, info, username):
        username_modified = username
        if username == "":
            users = list(User.objects.all())
            random_user = random.choice(users)
            while random_user.username == 'admin':
                random_user = random.choice(users)
            username_modified = random_user.username
        return Album.objects.filter(owner__username=username_modified).order_by('-created_at')


class OneAlbum(ObjectType):
    one_album = Field(AlbumType, id=String())

    def resolve_one_album(root, info, id):
        return Album.objects.get(id=id)


class PresignedUrl(ObjectType):
    presigned_url = Field(String, filename=String())

    def resolve_presigned_url(root, info, filename):
        return json.dumps(create_presigned_post(filename), separators=(',', ':'))


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
        if user.is_authenticated and user == album.owner:
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
        if user.is_authenticated and user == album.owner:
            setattr(album, 'name', name)
            album.save()
            return ModifyAlbum(album=album)
        else:
            return None


class AlbumQuery(PresignedUrl, AllAlbum, UserAlbum, OneAlbum):
    pass


class AlbumMutation(ObjectType):
    create_album = CreateAlbum.Field()
    delete_album = DeleteAlbum.Field()
    modify_album = ModifyAlbum.Field()
