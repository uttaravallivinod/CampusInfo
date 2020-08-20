# Generated by Django 2.2.10 on 2020-08-20 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, unique=True)),
                ('info', models.CharField(max_length=300)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
    ]
