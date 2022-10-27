# Generated by Django 4.0.8 on 2022-10-27 18:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0002_tasks'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharedTasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_only', models.BooleanField(default=False)),
                ('can_update', models.BooleanField(default=False)),
                ('tasks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todoapp.tasks')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
