# Generated by Django 2.1.10 on 2019-10-07 06:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TranslationTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('end_at', models.DateTimeField()),
                ('finished_at', models.DateTimeField(null=True)),
                ('source_language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_language', related_query_name='source_language', to='store.Language')),
                ('target_language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_language', related_query_name='target_language', to='store.Language')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translator', related_query_name='translator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
