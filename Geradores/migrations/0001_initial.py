# Generated by Django 4.1.5 on 2023-01-07 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Geradores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('uc', models.CharField(max_length=50)),
                ('status', models.IntegerField(default=1)),
            ],
        ),
    ]
