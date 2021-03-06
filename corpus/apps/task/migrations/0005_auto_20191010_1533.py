# Generated by Django 2.1.10 on 2019-10-10 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_auto_20191009_1711'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='translationtaskitem',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='translationtask',
            name='curr_item',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='task.TranslationTaskItem'),
        ),
        migrations.AddField(
            model_name='translationtaskitem',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='translationtask',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
