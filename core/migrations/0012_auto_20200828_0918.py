# Generated by Django 3.1 on 2020-08-28 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20200827_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='colors',
            field=models.CharField(choices=[('danger', 'Red'), ('success', 'Green'), ('info', 'Blue')], default='info', max_length=7),
        ),
    ]
