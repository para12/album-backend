# Generated by Django 3.2.6 on 2021-08-17 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=256)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('url', models.CharField(default='', max_length=256)),
                ('text', models.CharField(default='', max_length=256)),
                ('location', models.CharField(default='', max_length=256)),
                ('time', models.CharField(default='', max_length=256)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('album', models.ManyToManyField(default=None, related_name='album', to='app.Album')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RepresentitivePhoto',
            fields=[
                ('album', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.album')),
                ('photo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.photo')),
            ],
        ),
    ]