# Generated by Django 2.1.7 on 2019-03-04 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_auto_20190304_1909'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='accounts',
        ),
        migrations.AddField(
            model_name='account',
            name='client',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='register.Client'),
        ),
    ]
