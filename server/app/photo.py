from graphene import ObjectType, List, Field, String, Mutation, Date, Int
from graphene_django import DjangoObjectType

from .models import Photo, Album

import boto3

import logging
import os
from botocore.exceptions import ClientError
from botocore.config import Config

def delete_photo(object_name):

    s3_client = boto3.client('s3', aws_access_key_id=os.environ.get("S3_ACS_KEY"), aws_secret_access_key=os.environ.get(
        "S3_ACS_SEC"), config=Config(signature_version='s3v4'), region_name=os.environ.get("S3_REGION"))
    try:
        response = s3_client.delete_object(Bucket=os.environ.get("S3_BUCKET_NAME"), Key=object_name)  
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response

class PhotoType(DjangoObjectType):
    class Meta:
        model = Photo
        fields= '__all__'


class AllPhoto(ObjectType):
    all_photos = List(PhotoType)
    def resolve_all_photos(root, info):
        return Photo.objects.all()

class AlbumPhotos(ObjectType):
    album_photos = Field(List(PhotoType), albumId=String())
    def resolve_album_photos(root, info, albumId):
        return Photo.objects.filter(album__id=albumId).order_by('-created_at')


class AddPhoto(Mutation):
    class Arguments:
        url = String()
        text = String()
        location = String()
        time = Date() or None
        width = Int() or None
        height = Int() or None
        albumId = String()
    photo = Field(PhotoType)
    def mutate(root, info, url, text, location, time, width, height, albumId):
        user = info.context.user
        if user.is_authenticated :
            album = Album.objects.get(id=albumId)
            photo = Photo.objects.create(url=url, text=text, location=location, time=time, width=width, height=height, owner=user, album=album)
            photo.save()
            return AddPhoto(photo=photo)
        else:
            return None

class DeletePhoto(Mutation):
    class Arguments:
        id = String()
    photo = Field(PhotoType)

    def mutate(root, info, id):
        user = info.context.user
        photo = Photo.objects.get(id=id)
        original = Photo.objects.get(id=id)
        if user.is_authenticated and user == photo.owner:
            response = delete_photo(photo.url)
            photo.delete()
            return DeletePhoto(photo=original)
        else:
            return None

class ModifyPhoto(Mutation):
    class Arguments:
        id = String()
        location = String()
        text = String()
        time = Date() or None

    photo = Field(PhotoType)

    def mutate(root, info, id, location, text, time):
        user = info.context.user
        photo = Photo.objects.get(id=id)
        if user.is_authenticated and user == photo.owner:
            setattr(photo, 'location', location)
            setattr(photo, 'text', text)
            setattr(photo, 'time', time)
            photo.save()
            return ModifyPhoto(photo=photo)
        else:
            return None

class PhotoQuery(AllPhoto, AlbumPhotos):
    pass


class PhotoMutation(ObjectType):
    add_photo = AddPhoto.Field()
    delete_photo = DeletePhoto.Field()
    modify_photo = ModifyPhoto.Field()
    pass