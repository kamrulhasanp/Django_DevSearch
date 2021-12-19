# Generated by Django 3.2.6 on 2021-12-15 18:13

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_profiles_locations'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('subject', models.CharField(blank=True, max_length=200, null=True)),
                ('body', models.TextField()),
                ('is_read', models.BooleanField(default=False, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('recipient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to='users.profiles')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.profiles')),
            ],
            options={
                'ordering': ['is_read', '-created'],
            },
        ),
    ]
