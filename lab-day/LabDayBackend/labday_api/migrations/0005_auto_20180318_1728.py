# Generated by Django 2.0.2 on 2018-03-18 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
            ('labday_api', '0004_auto_20180318_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='path',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='labday_api.Path'),
        ),
    ]
