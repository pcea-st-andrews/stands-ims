# Generated by Django 3.2.7 on 2021-10-19 07:30

from django.db import migrations

import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0004_alter_person_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                max_length=128, null=True, region=None
            ),
        ),
    ]
