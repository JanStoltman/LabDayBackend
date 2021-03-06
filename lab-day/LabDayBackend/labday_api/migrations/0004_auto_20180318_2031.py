# Generated by Django 2.0.2 on 2018-03-18 20:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('labday_api', '0003_userpasswordchanges'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password_used', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('path', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='labday_api.Path')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='userpasswordchanges',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserPasswordChanges',
        ),
    ]
