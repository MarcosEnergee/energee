# Generated by Django 4.1.5 on 2023-01-07 20:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Administradores', '0001_initial'),
        ('Geradores', '0002_geradores_distribuidora'),
    ]

    operations = [
        migrations.AddField(
            model_name='geradores',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Administradores.administradores'),
        ),
    ]
