# Generated by Django 2.1.10 on 2019-10-11 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_translationtask_total_word_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='translationtask',
            old_name='total_word_count',
            new_name='word_count',
        ),
    ]
