# Generated by Django 4.1.5 on 2023-03-14 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Geradores', '0006_geradores_senha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geradores',
            name='senha',
            field=models.CharField(max_length=100),
        ),
    ]
