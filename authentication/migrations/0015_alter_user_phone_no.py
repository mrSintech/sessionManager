# Generated by Django 4.1 on 2022-08-27 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0014_alter_admin_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_no',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='authentication.userphonenumber'),
        ),
    ]