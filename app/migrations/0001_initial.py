# Generated by Django 4.1.1 on 2022-09-22 16:52

from django.conf import settings
import django.core.validators
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
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cat_name', models.CharField(max_length=70, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('place_name', models.CharField(max_length=70, verbose_name='name')),
                ('governorate', models.CharField(max_length=70, verbose_name='governorate')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category', verbose_name='category')),
            ],
        ),
        migrations.CreateModel(
            name='Reels',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('en_video', models.FileField(upload_to='video', validators=[django.core.validators.FileExtensionValidator(['mp4'])])),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('favourite', models.ManyToManyField(related_name='favourite', through='app.Likes', to=settings.AUTH_USER_MODEL)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.place', verbose_name='place')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.AddField(
            model_name='likes',
            name='reel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.reels'),
        ),
        migrations.AddField(
            model_name='likes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('comm_date', models.DateField(auto_now_add=True, verbose_name='date')),
                ('comment', models.CharField(max_length=500)),
                ('reel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.reels')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
