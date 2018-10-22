#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

GENDER = (
    (0, 'Masculino'),
    (1, 'Femenino')
)

HAND = (
    (0, 'Derecho'),
    (1, 'Izquierdo'),
    (2, 'Ambos'),
)

PAIN_SIDE = (
    (0, 'Lado izquierdo'),
    (1, 'Lado derecho'),
    (2, 'Ambos'),
)

PAIN_WHEN = (
    (0, 'Al realizar mi trabajo'),
    (1, 'Al final del dia'),
    (2, 'En mi casa'),
    (3, 'Todo el tiempo'),
    (4, 'Al final de la semana')
)

PAIN_PRESENTED_HOW = (
    (0, 'Dolor'),
    (1, 'Hormigueo'),
    (2, 'Malestar'),
    (3, 'Adormecimiento'),
)

PAIN_AGO = (
    (0, '1 semana'),
    (1, '1 mes'),
    (2, '3 meses'),
    (3, '6 meses'),
    (4, '12 meses'),
    (5, 'Mas de 12 meses')
)

PAIN_DURATION = (
    (0, 'Menos de 24 horas'),
    (1, 'De 1 a 7 dias'),
    (2, 'De 8 a 30 dias'),
    (3, 'De manera permanente'),
    (4, 'De manera intermitente')
)

PAIN_INTENSITY = (
    (0, '0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
)

PAIN_LEVEL = (
    (0, 'Nada'),
    (1, 'Un poco incomodo'),
    (2, 'Moderamente incomodo'),
    (3, 'Muy incomodo')
)

PAIN_LEVEL_WORK = (
    (0, 'No, en lo absoluto'),
    (1, 'Poca interferencia'),
    (2, 'Interfiere sustancialmente')
)

FREQUENCY = (
    (0, '15 min'),
    (1, '30 min'),
    (2, '1 hora'),
    (3, 'Mas de una hora')
)

DURATION = (
    (0, 'Diario'),
    (1, 'Dos veces a la semana'),
    (2, 'Tres veces a la semana'),
    (3, 'Fines de semana')
)

YES_NO = (
    (0, 'Si'),
    (1, 'No')
)

HOW_MUCH_CIGARETTES = (
    (0, 'De 1 a 5 cigarrillos'),
    (1, 'De 6 a 15 cigarrillos'),
    (2, '16 o mas cigarrillos'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9')
)

JOB_JOURNEY = (
    (0, '0H - 1H'),
    (1, '1H - 2H'),
    (2, '2H - 4H'),
    (3, '4H - 6H'),
    (4, '8H'),
    (5, '12H'),
    (6, 'Otro')
)

class City(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Nombre")

    def __str__(self):
        return "%s" % self.name

    def __unicode__(self):
        return u'%s' % self.name

class Company(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Nombre")
    user = models.ForeignKey(User, null=True, blank=True ,verbose_name='Encuestador', on_delete=models.SET_NULL)
    nit = models.CharField(max_length=200, null=True, blank=True, verbose_name="NIT")
    date = models.DateField(null=True, blank=True, verbose_name='Fecha de constitucion')
    city = models.CharField(max_length=200, null=True, blank=True, verbose_name="Ciudad")
    department = models.CharField(max_length=200, null=True, blank=True, verbose_name="Departamento")

    def __str__(self):
        return "%s" % self.name

    def __unicode__(self):
        return u'%s' % self.name

class Worker(models.Model):
    company = models.ForeignKey(Company, null=True, verbose_name='Empresa', on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Nombre")
    lastname = models.CharField(max_length=200, null=True, blank=True, verbose_name="Apellido")
    identification = models.CharField(max_length=200, null=True, blank=True, verbose_name="Identificacion")
    weight = models.CharField(max_length=200, null=True, blank=True, verbose_name="Peso (KG)")
    height = models.CharField(max_length=200, null=True, blank=True, verbose_name="Altura (CM)")
    gender = models.IntegerField(choices=GENDER, null=True, blank=True, verbose_name='Sexo')
    hand = models.IntegerField(choices=HAND,null=True, blank=True, verbose_name='Dominancia')
    age = models.CharField(max_length=200, null=True, blank=True, verbose_name="Edad")
    monthsCompany = models.CharField(max_length=200, null=True, blank=True, verbose_name="Meses en la empresa")
    yearsCompany = models.CharField(max_length=200, null=True, blank=True, verbose_name="Años en la empresa")
    dependency = models.CharField(max_length=200, null=True, blank=True, verbose_name="Area o dependencia")
    smoke = models.IntegerField(choices=YES_NO, null=True, blank=True, verbose_name='¿Fumas?')
    how_much_cigarettes = models.IntegerField(choices=HOW_MUCH_CIGARETTES, null=True, blank=True, verbose_name='¿Cuantos cigarrillos al dia?')
    how_much_smoke = models.CharField(max_length=200, null=True, blank=True, verbose_name="¿Hace cuanto tiempo fuma?")
    physical_activity_question = models.IntegerField(choices=YES_NO, null=True, blank=True, verbose_name='¿Realiza actividad fisica?')
    physical_activity = models.CharField(max_length=200, null=True, blank=True, verbose_name="¿Cual?")
    frequency = models.IntegerField(choices=FREQUENCY, null=True, blank=True, verbose_name='Frecuencia')
    duration = models.IntegerField(choices=DURATION, null=True, blank=True, verbose_name='Duracion')
    job_journey = models.IntegerField(choices=JOB_JOURNEY, null=True, blank=True, verbose_name='¿Cual es su jornada laboral?')
    vialbility_job_journey = models.IntegerField(choices=YES_NO, null=True, blank=True, verbose_name='¿La duracion semanal de la jornada es variable?')
    how_much_hours_work = models.CharField(max_length=200, null=True, blank=True, verbose_name="¿Cuantas horas trabaja por dia?")
    explanation_job_hours = models.CharField(max_length=200, null=True, blank=True, verbose_name="Explique")
    inconvenience_body = models.IntegerField(choices=YES_NO, null=True, blank=True, verbose_name='¿Durante los ultimos 7 dias ha presentado dolor, molestias o inconfort en alguna parte del cuerpo?')
    sickness = models.IntegerField(choices=YES_NO, null=True, blank=True, verbose_name='¿Durante los ultimos 7 dias, Usted ha presentado alguna enfermedad?')
    sick = models.CharField(max_length=200, null=True, blank=True, verbose_name="¿Cual?")
    sick_observations = models.CharField(max_length=200, null=True, blank=True, verbose_name="Observaciones")

    def __str__(self):
        return "%s" % (self.name + " " + self.lastname)

    def __unicode__(self):
        return u'%s' % self.name

class BodyPart(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Nombre")

    def __str__(self):
        return "%s" % self.name

    def __unicode__(self):
        return u'%s' % self.name

class BodyPartForm(models.Model):
    bodyPart = models.ForeignKey(BodyPart, null=True, verbose_name='Parte del cuerpo', on_delete=models.SET_NULL)
    paiSide = models.IntegerField(choices=PAIN_SIDE, null=True, blank=True, verbose_name='Frecuencia')
    painWhen = models.IntegerField(choices=PAIN_WHEN, null=True, blank=True, verbose_name='Frecuencia')
    painPresentedHow = models.IntegerField(choices=PAIN_PRESENTED_HOW, null=True, blank=True, verbose_name='Frecuencia')
    painAgo = models.IntegerField(choices=PAIN_AGO, null=True, blank=True, verbose_name='Frecuencia')
    painDuration = models.IntegerField(choices=PAIN_DURATION, null=True, blank=True, verbose_name='Frecuencia')
    painIntensity = models.IntegerField(choices=PAIN_INTENSITY, null=True, blank=True, verbose_name='Frecuencia')
    painLevel = models.IntegerField(choices=PAIN_LEVEL, null=True, blank=True, verbose_name='Frecuencia')
    painLevelWork = models.IntegerField(choices=PAIN_LEVEL_WORK, null=True, blank=True, verbose_name='Frecuencia')
    observations = models.CharField(max_length=200, null=True, blank=True, verbose_name="Observaciones")

class FilledForms(models.Model):
    worker = models.ForeignKey(Worker, null=True, verbose_name='Trabajador', on_delete=models.SET_NULL)
    filledForms = models.ManyToManyField(BodyPartForm, null=True, blank=True, verbose_name='Formularios asociados')
