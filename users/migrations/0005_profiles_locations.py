# Generated by Django 3.2.6 on 2021-11-11 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_skill_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiles',
            name='locations',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]