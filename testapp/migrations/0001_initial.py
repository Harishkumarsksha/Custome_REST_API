# Generated by Django 3.0.5 on 2020-04-22 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eno', models.IntegerField(null=True)),
                ('ename', models.CharField(max_length=200, null=True)),
                ('esal', models.CharField(max_length=200, null=True)),
                ('eaddr', models.TextField(max_length=500, null=True)),
            ],
        ),
    ]