# Generated by Django 3.2.5 on 2021-10-24 14:14

from django.db import migrations


def delete_temperature_records(apps, schema_editor):
    TemperatureRecord = apps.get_model("records", "TemperatureRecord")
    null_person_records = TemperatureRecord.objects.filter(person__dob__isnull=True)
    print(f"Temp records pending deletion: {null_person_records.count()}")
    null_person_records.delete()


def delete_people_records(apps, schema_editor):
    Person = apps.get_model("people", "Person")
    null_personal_records = Person.objects.filter(dob__isnull=True)
    print(f"People records pending deletion: {null_personal_records.count()}")
    null_personal_records.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0004_auto_20210714_1800"),
        ("records", "0005_rename_temp_temperaturerecord_body_temperature"),
    ]

    operations = [
        migrations.RunPython(delete_temperature_records),
        migrations.RunPython(delete_people_records),
    ]
