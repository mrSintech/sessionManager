# Generated by Django 4.1 on 2022-08-24 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_roominfo_ikey_roominfo_ivalue'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roominfo',
            old_name='ikey',
            new_name='key',
        ),
        migrations.RenameField(
            model_name='roominfo',
            old_name='ivalue',
            new_name='value',
        ),
    ]
