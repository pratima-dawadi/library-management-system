# Generated by Django 5.2.3 on 2025-06-28 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('librarian', 'Librarian'), ('user', 'User')], default='user', max_length=20),
        ),
    ]
