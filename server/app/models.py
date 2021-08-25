from django.db import models
from django.contrib.auth.models import User
import uuid

class Album(models.Model) :
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256, default="")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Photo(models.Model) :
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.CharField(max_length=256, default="")
    text = models.CharField(max_length=256, default="")
    location = models.CharField(max_length=256, default="")
    time = models.CharField(max_length=256, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ManyToManyField(Album, related_name='album', default=None)

class RepresentitivePhoto(models.Model) :
    album = models.OneToOneField(Album, on_delete=models.CASCADE, primary_key=True)
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE)

# class Like(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     like = models.BooleanField(default=True)
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

# class Comment(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
#     comment = models.CharField(max_length=256, default="")
#     created_at = models.DateTimeField(auto_now_add=True)