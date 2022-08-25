# Generated by Django 4.1 on 2022-08-24 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_user_departman'),
        ('core', '0016_reserve_date_created_sessionroom_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserve',
            name='departman',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reserves', to='authentication.departman'),
        ),
    ]