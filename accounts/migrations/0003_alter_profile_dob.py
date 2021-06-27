# Generated by Django 3.2.4 on 2021-06-27 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_auto_20210626_1528"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="dob",
            field=models.DateField(
                blank=True,
                help_text="The format should be DD/MM/YYYY",
                null=True,
                verbose_name="date of birth",
            ),
        ),
    ]
