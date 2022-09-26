# Generated by Django 4.1.1 on 2022-09-22 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='category',
        ),
        migrations.AlterField(
            model_name='reels',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.place', verbose_name='place'),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Place',
        ),
    ]