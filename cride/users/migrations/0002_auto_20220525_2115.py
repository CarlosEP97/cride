# Generated by Django 2.0.10 on 2022-05-25 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_verfied',
            new_name='is_verified',
        ),
    ]