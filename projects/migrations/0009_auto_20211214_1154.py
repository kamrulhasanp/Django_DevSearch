# Generated by Django 3.2.6 on 2021-12-14 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_profiles_locations'),
        ('projects', '0008_alter_project_featured_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='review',
            name='woner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profiles'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('woner', 'project')},
        ),
    ]
