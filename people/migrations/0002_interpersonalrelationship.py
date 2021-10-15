# Generated by Django 3.2.7 on 2021-10-15 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("people", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="InterpersonalRelationship",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "relation",
                    models.CharField(
                        choices=[
                            ("R", "Romantic"),
                            ("M", "Marital"),
                            ("PC", "Parent-child"),
                            ("S", "Sibling"),
                        ],
                        help_text="How the person and the relative are associated.",
                        max_length=2,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        help_text="The user who created this record.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="relationships",
                        to="people.person",
                    ),
                ),
                (
                    "relative",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reverse_relationships",
                        to="people.person",
                    ),
                ),
            ],
            options={
                "db_table": "people_relationship",
                "ordering": ["person__username"],
            },
        ),
    ]
