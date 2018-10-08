# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BodyPart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True, verbose_name=b'Nombre', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='BodyPartForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('paiSide', models.IntegerField(blank=True, null=True, verbose_name=b'Frecuencia', choices=[(0, b'Lado izquierdo'), (1, b'Lado derecho'), (2, b'Ambos')])),
                ('painWhen', models.IntegerField(blank=True, null=True, verbose_name=b'Frecuencia', choices=[(0, b'Al realizar mi trabajo'), (1, b'Al final del dia'), (2, b'En mi casa'), (3, b'Todo el tiempo'), (4, b'Al final de la semana')])),
                ('painPresentedHow', models.IntegerField(blank=True, null=True, verbose_name=b'Frecuencia', choices=[(0, b'Dolor'), (1, b'Hormigueo'), (2, b'Malestar'), (3, b'Adormecimiento')])),
                ('painAgo', models.IntegerField(blank=True, null=True, verbose_name=b'Frecuencia', choices=[(0, b'1 semana'), (1, b'1 mes'), (2, b'3 meses'), (3, b'6 meses'), (4, b'12 meses'), (5, b'Mas de 12 meses')])),
                ('painDuration', models.IntegerField(blank=True, null=True, verbose_name=b'Frecuencia', choices=[(0, b'Menos de 24 horas'), (1, b'De 1 a 7 dias'), (2, b'De 8 a 30 dias'), (3, b'De manera permanente'), (4, b'De manera intermitente')])),
                ('painIntensity', models.IntegerField(blank=True, null=True, verbose_name=b'Frecuencia', choices=[(0, b'0'), (1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5'), (6, b'6'), (7, b'7'), (8, b'8'), (9, b'9'), (10, b'10')])),
                ('painLevel', models.IntegerField(blank=True, null=True, verbose_name=b'Frecuencia', choices=[(0, b'Nada'), (1, b'Un poco incomodo'), (2, b'Moderamente incomodo'), (3, b'Muy incomodo')])),
                ('painLevelWork', models.IntegerField(blank=True, null=True, verbose_name=b'Frecuencia', choices=[(0, b'No, en lo absoluto'), (1, b'Poca interferencia'), (2, b'Interfiere sustancialmente')])),
                ('observations', models.CharField(max_length=200, null=True, verbose_name=b'Observaciones', blank=True)),
                ('bodyPart', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Parte del cuerpo', to='api.BodyPart', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True, verbose_name=b'Nombre', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True, verbose_name=b'Nombre', blank=True)),
                ('nit', models.CharField(max_length=200, null=True, verbose_name=b'NIT', blank=True)),
                ('date', models.DateField(null=True, verbose_name=b'Fecha de constitucion', blank=True)),
                ('city', models.CharField(max_length=200, null=True, verbose_name=b'Ciudad', blank=True)),
                ('department', models.CharField(max_length=200, null=True, verbose_name=b'Departamento', blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Encuestador', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FilledForms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filledForms', models.ManyToManyField(to='api.BodyPartForm', null=True, verbose_name=b'Formularios asociados', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True, verbose_name=b'Nombre', blank=True)),
                ('lastname', models.CharField(max_length=200, null=True, verbose_name=b'Apellido', blank=True)),
                ('identification', models.CharField(max_length=200, null=True, verbose_name=b'Identificacion', blank=True)),
                ('weight', models.CharField(max_length=200, null=True, verbose_name=b'Peso (KG)', blank=True)),
                ('height', models.CharField(max_length=200, null=True, verbose_name=b'Altura (CM)', blank=True)),
                ('gender', models.IntegerField(blank=True, null=True, verbose_name=b'Sexo', choices=[(0, b'Masculino'), (1, b'Femenino')])),
                ('hand', models.IntegerField(blank=True, null=True, verbose_name=b'Dominancia', choices=[(0, b'Derecho'), (1, b'Izquierdo'), (2, b'Ambos')])),
                ('age', models.CharField(max_length=200, null=True, verbose_name=b'Edad', blank=True)),
                ('monthsCompany', models.CharField(max_length=200, null=True, verbose_name=b'Meses en la empresa', blank=True)),
                ('yearsCompany', models.CharField(max_length=200, null=True, verbose_name=b'A\xc3\xb1os en la empresa', blank=True)),
                ('dependency', models.CharField(max_length=200, null=True, verbose_name=b'Area o dependencia', blank=True)),
                ('smoke', models.IntegerField(blank=True, null=True, verbose_name=b'\xc2\xbfFumas?', choices=[(0, b'Si'), (1, b'No')])),
                ('how_much_cigarettes', models.IntegerField(blank=True, null=True, verbose_name=b'\xc2\xbfCuantos cigarrillos al dia?', choices=[(0, b'0'), (1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5'), (6, b'6'), (7, b'7'), (8, b'8'), (9, b'9')])),
                ('how_much_smoke', models.CharField(max_length=200, null=True, verbose_name=b'\xc2\xbfHace cuanto tiempo fuma?', blank=True)),
                ('physical_activity_question', models.IntegerField(blank=True, null=True, verbose_name=b'\xc2\xbfRealiza actividad fisica?', choices=[(0, b'Si'), (1, b'No')])),
                ('physical_activity', models.CharField(max_length=200, null=True, verbose_name=b'\xc2\xbfCual?', blank=True)),
                ('frequency', models.IntegerField(blank=True, null=True, verbose_name=b'Frecuencia', choices=[(0, b'15 min'), (1, b'30 min'), (2, b'1 hora'), (3, b'Mas de una hora')])),
                ('duration', models.IntegerField(blank=True, null=True, verbose_name=b'Duracion', choices=[(0, b'Diario'), (1, b'Dos veces a la semana'), (2, b'Tres veces a la semana'), (3, b'Fines de semana')])),
                ('job_journey', models.IntegerField(blank=True, null=True, verbose_name=b'\xc2\xbfCual es su jornada laboral?', choices=[(0, b'0H - 1H'), (1, b'1H - 2H'), (2, b'2H - 4H'), (3, b'4H - 6H'), (4, b'8H'), (5, b'12H'), (6, b'Otro')])),
                ('vialbility_job_journey', models.IntegerField(blank=True, null=True, verbose_name=b'\xc2\xbfLa duracion semanal de la jornada es variable?', choices=[(0, b'Si'), (1, b'No')])),
                ('how_much_hours_work', models.CharField(max_length=200, null=True, verbose_name=b'\xc2\xbfCuantas horas trabaja por dia?', blank=True)),
                ('explanation_job_hours', models.CharField(max_length=200, null=True, verbose_name=b'Explique', blank=True)),
                ('inconvenience_body', models.IntegerField(blank=True, null=True, verbose_name=b'\xc2\xbfDurante los ultimos 7 dias ha presentado dolor, molestias o inconfort en alguna parte del cuerpo?', choices=[(0, b'Si'), (1, b'No')])),
                ('sickness', models.IntegerField(blank=True, null=True, verbose_name=b'\xc2\xbfDurante los ultimos 7 dias, Usted ha presentado alguna enfermedad?', choices=[(0, b'Si'), (1, b'No')])),
                ('sick', models.CharField(max_length=200, null=True, verbose_name=b'\xc2\xbfCual?', blank=True)),
                ('sick_observations', models.CharField(max_length=200, null=True, verbose_name=b'Observaciones', blank=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Empresa', to='api.Company', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='filledforms',
            name='worker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Trabajador', to='api.Worker', null=True),
        ),
    ]
