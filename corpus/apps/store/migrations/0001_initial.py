# Generated by Django 2.1.10 on 2019-10-07 06:57

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionnary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=uuid.uuid4, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('dictionnary', models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Dictionnary')),
            ],
        ),
    ]
