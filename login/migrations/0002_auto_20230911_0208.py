# Generated by Django 3.2.5 on 2023-09-11 02:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='datosusuario',
            name='biography',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='datosusuario',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
        migrations.CreateModel(
            name='SocialAccounts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('link', models.CharField(max_length=300)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
