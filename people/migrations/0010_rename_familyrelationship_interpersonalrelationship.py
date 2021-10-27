# Generated by Django 3.2.7 on 2021-10-27 14:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("people", "0009_update_familyrelationship_meta"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="FamilyRelationship",
            new_name="InterpersonalRelationship",
        ),
        migrations.RemoveConstraint(
            model_name="interpersonalrelationship",
            name="people_unique_familyrelationship",
        ),
        migrations.AddConstraint(
            model_name="interpersonalrelationship",
            constraint=models.UniqueConstraint(
                fields=("person", "relative"),
                name="people_unique_interpersonalrelationship",
            ),
        ),
    ]