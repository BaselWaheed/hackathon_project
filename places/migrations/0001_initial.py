# Generated by Django 4.1.1 on 2022-09-22 20:40

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            name='Place',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('place_name', models.CharField(max_length=70, verbose_name='name')),
                ('governorate', models.CharField(max_length=70, verbose_name='governorate')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.category', verbose_name='category')),
            ],
        ),
    ]
