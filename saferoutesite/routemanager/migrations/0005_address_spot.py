# Generated by Django 2.1.5 on 2019-03-10 20:20

from django.db import migrations
import djgeojson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('routemanager', '0004_route_safety_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='spot',
            field=djgeojson.fields.PointField(default=(0, 0)),
            preserve_default=False,
        ),
    ]