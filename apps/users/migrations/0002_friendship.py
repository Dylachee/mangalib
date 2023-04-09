# Generated by Django 4.2 on 2023-04-09 18:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('users', models.ManyToManyField(related_name='friends', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Дружба',
                'verbose_name_plural': 'Дружбы',
            },
        ),
    ]