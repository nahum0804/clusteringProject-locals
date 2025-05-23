# Generated by Django 5.2.1 on 2025-05-21 02:03

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id_cliente', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cedula', models.CharField(max_length=15, unique=True)),
                ('nombre_completo', models.CharField(max_length=100)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('correo', models.EmailField(blank=True, max_length=254, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('saldo_actual', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('id_ruta', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_salida', models.DateField()),
                ('conductor', models.CharField(max_length=100)),
                ('observacion', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('placa', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=30)),
                ('capacidad_kg', models.DecimalField(decimal_places=2, max_digits=6)),
                ('disponible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ControlEnvio',
            fields=[
                ('id_paquete', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('destino', models.CharField(max_length=150)),
                ('peso', models.DecimalField(decimal_places=2, max_digits=6)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(default='pendiente', max_length=20)),
                ('qr_generado', models.TextField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_local.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='HistorialEnvio',
            fields=[
                ('id_envio', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fecha_envio', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(max_length=20)),
                ('costo_envio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('qr_codigo', models.TextField()),
                ('cliente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_local.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='HistorialPago',
            fields=[
                ('id_pago', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_pago', models.DateTimeField(auto_now_add=True)),
                ('medio_pago', models.CharField(max_length=50)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_local.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleRuta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entregado', models.BooleanField(default=False)),
                ('paquete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_local.controlenvio')),
                ('ruta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_local.ruta')),
            ],
        ),
        migrations.AddField(
            model_name='ruta',
            name='vehiculo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_local.vehiculo'),
        ),
    ]
