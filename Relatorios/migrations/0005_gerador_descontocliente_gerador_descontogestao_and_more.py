# Generated by Django 4.1.5 on 2023-06-06 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Relatorios', '0004_gerador_imposto_gerador_celesc_imposto'),
    ]

    operations = [
        migrations.AddField(
            model_name='gerador',
            name='descontoCliente',
            field=models.IntegerField(default=0, max_length=5),
        ),
        migrations.AddField(
            model_name='gerador',
            name='descontoGestao',
            field=models.IntegerField(default=0, max_length=5),
        ),
        migrations.AddField(
            model_name='gerador_celesc',
            name='descontoCliente',
            field=models.IntegerField(default=0, max_length=5),
        ),
        migrations.AddField(
            model_name='gerador_celesc',
            name='descontoGestao',
            field=models.IntegerField(default=0, max_length=5),
        ),
    ]
