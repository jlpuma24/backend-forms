#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, Http404
from django.contrib.auth import authenticate
from api.models import *
import datetime
import json
from matplotlib import pylab
from pylab import *
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import PIL, PIL.Image, StringIO

@csrf_exempt
def grapsHttpResponse(request, ageReport):
    if request.method == "GET":
        titleX = ''
        titleGraph = ''
        if int(ageReport) == 1:
            titleX = 'Edad'
            titleGraph = 'Edad'
        elif int(ageReport) == 2:
            titleX = 'Peso'
            titleGraph = 'Peso'
        elif int(ageReport) == 3:
            titleX = 'Estatura'
            titleGraph = 'Estatura'
        elif int(ageReport) == 4:
            titleX = 'IMC'
            titleGraph = 'IMC'
        elif int(ageReport) == 5:
            titleX = 'Antiguedad en el cargo'
            titleGraph = 'Antiguedad en el cargo'
        elif int(ageReport) == 6:
            titleX = 'EN SU TRABAJO ACTUAL, ¿CUANTAS HORAS TRABAJA USTED POR DIA?'
            titleGraph = 'EN SU TRABAJO ACTUAL, ¿CUANTAS HORAS TRABAJA USTED POR DIA?'

        # Construct the graph
        #x = arange(0, 2*pi, 0.01)
        #s = cos(x)**2
        #plot(x, s)

        #xlabel('xlabel(X)')
        #ylabel('ylabel(Y)')
        #title('Simple Graph!')
        #grid(True)

        mu, sigma = 10, 15
        x = mu + sigma*np.random.randn(20)
        #x = [0, 5, 20, 35, 50]

        # x = datos
        # alpha = claridad de la grafica
        # facecolor = color

        n, bins, patches = plt.hist(x, normed=1, facecolor='green', alpha=0.90)

        # add a 'best fit' line
        y = mlab.normpdf( bins, mu, sigma)
        l = plt.plot(bins, y, 'r--', linewidth=1)

        plt.xlabel(titleX)
        plt.ylabel('Densidad')
        plt.title(titleGraph)
        #xmin, xmax, ymin, ymax (Direccion de los ejes)
        #xmin = 0 siempre
        #xmax = max cantidad en escala acorde a reporte
        #ymin = 0 siempre.
        #ymax = Varia acorde a reporte.
        plt.axis([0, 50, 0, 0.10])
        plt.grid(True)

        # Store image in a string buffer
        buffer = StringIO.StringIO()
        canvas = pylab.get_current_fig_manager().canvas
        canvas.draw()
        pilImage = PIL.Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
        pilImage.save(buffer, "PNG")
        pylab.close()

        # Send buffer in a http response the the browser with the mime type image/png set
        return HttpResponse(buffer.getvalue(), content_type="image/png")

@csrf_exempt
def employeeReport(request):
    if request.method == "POST":
        bodyUnicode = request.body.decode('utf-8')
        body = json.loads(bodyUnicode)
        try:
            employeeObject = Worker.objects.filter(identification=body["identification"]).first()
            if employeeObject:
                imc = float(employeeObject.weight) / float(employeeObject.height)

                d1Report = {"imc": imcPoint(round(imc,2)),
                "charge": chargePoint(employeeObject.dependency),
                "years": yearsPoint(int(employeeObject.yearsCompany)),
                "age": agePoint(int(employeeObject.age)),
                "dominance": 1,
                "gender": genderPoint(int(employeeObject.gender))}

                d2Report = {"frequencyPhysicalActivity": frequencyPhysicalActivityPoint(int(employeeObject.frequency)),
                "durationPhysicalActivity": durationPhysicalActivityPoint(int(employeeObject.duration)),
                "howMuchSmoke": howMuchSmokePoint(employeeObject.how_much_smoke),
                "cigarrettes": cigarrettesQuantityPoint(employeeObject.how_much_cigarettes)}

                d3Report = {"workedHours": workedHoursPoint(int(employeeObject.how_much_hours_work)),
                "weekDuration": weekDurationPoint(int(employeeObject.vialbility_job_journey)),
                "polifunctionality": 5}

                workerFormsDict = FilledForms.objects.get(worker=employeeObject)
                d4ReportDict = []

                for workerFormObject in workerFormsDict.filledForms.all():
                    d4ReportDict.append({"bodyPart": workerFormObject.bodyPart.name,
                    "painPresentedHow": painPresentedHowScore(int(workerFormObject.painPresentedHow)),
                    "painWhen": painWhenScore(int(workerFormObject.painWhen)),
                    "painAgo": painAgoScore(int(workerFormObject.painAgo)),
                    "painDuration": painDurationScore(int(workerFormObject.painDuration)),
                    "painIntensity": painIntensityScore(int(workerFormObject.painIntensity))})

                return HttpResponse(json.dumps({"status": "OK", "message": "", "d1Report": d1Report, "d2Report": d2Report, "d3Report": d3Report, "d4Report": d4ReportDict}), content_type="application/json")
            else:
                return HttpResponse(json.dumps({"status": "ERROR", "error": "Invalid method", "message": "El reporte para este usuario no fue encontrado"}), content_type="application/json")
        except Exception:
            return HttpResponse(json.dumps({"status": "ERROR", "error": "Invalid method", "message": "El reporte para este usuario no fue encontrado"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"status": "ERROR", "error": "Invalid method", "message": "El reporte para este usuario no fue encontrado"}), content_type="application/json")

def dump(obj):
   for attr in dir(obj):
       if hasattr( obj, attr ):
           print( "obj.%s = %s" % (attr, getattr(obj, attr)))

def painIntensityScore(score):
    if score >= 1 and score <= 3:
        return 2
    elif score >= 4 and score <= 7:
        return 3
    else:
        return 5

def painDurationScore(score):
    if score == 0:
        return 2
    elif score == 1:
        return 3
    elif score == 2:
        return 4
    else:
        return 5

def painAgoScore(score):
    if score == 0:
        return 1
    elif score == 1:
        return 2
    elif score == 2:
        return 3
    elif score == 3:
        return 4
    else:
        return 5

def painWhenScore(score):
    if score == 0:
        return 4
    elif score == 1:
        return 3
    elif score == 2:
        return 1
    elif score == 3:
        return 5
    else:
        return 2

def painPresentedHowScore(score):
    if score == 0:
        return 5
    elif score == 1:
        return 4
    elif score == 2:
        return 3
    else:
        return 2

def weekDurationPoint(score):
    if score == 0:
        return 5
    if workedHours >= 1 and workedHours <= 4:
        return 2
    elif workedHours >= 5 and workedHours <= 8:
        return 3
    elif workedHours >= 8 and workedHours <= 12:
        return 4
    else:
        return 5

def howMuchSmokePoint(howMuchSmoke):
    if "Menos" in howMuchSmoke or "Less" in howMuchSmoke:
        return 1
    elif "1 a" in howMuchSmoke or "1 to" in howMuchSmoke:
        return 2
    elif "3 a" in howMuchSmoke or "3 to" in howMuchSmoke:
        return 3
    elif "5 a" in howMuchSmoke or "5 to" in howMuchSmoke:
        return 4
    else:
        return 5

def durationPhysicalActivityPoint(score):
    if score == 0:
        return 1
    elif score == 1:
        return 2
    elif score == 2:
        return 3
    else:
        return 4

def frequencyPhysicalActivityPoint(score):
    if score == 0:
        return 5
    elif score == 1:
        return 4
    elif score == 2:
        return 3
    else:
        return 2

def cigarrettesQuantityPoint(score):
    if score == 0:
        return 3
    elif score == 1:
        return 4
    else:
        return 5

def imcPoint(imc):
    if imc < 18.50:
        return 5
    elif imc >=18.50 and imc <= 24.90:
        return 1
    elif imc >= 25.00 and imc <= 29.90:
        return 2
    elif imc >= 30.00 and imc <= 34.90:
        return 3
    elif imc >= 35.00 and imc <= 39.90:
        return 4
    else:
        return 5

def chargePoint(dependency):
    if "Op" in dependency:
        return 5
    elif "Sup" in dependency:
        return 4
    else:
        return 3

def yearsPoint(years):
    if years < 1:
        return 1
    elif years >= 1 and years <= 5:
        return 2
    elif years >= 6 and years <= 10:
        return 3
    elif years >= 11 and years <= 15:
        return 4
    else:
        return 5

def agePoint(age):
    if age >= 18 and age <= 25:
        return 1
    elif age >= 26 and age <= 35:
        return 2
    elif age >= 36 and age <= 45:
        return 3
    elif age >= 46 and age <= 55:
        return 4
    else:
        return 5

def genderPoint(gender):
    if gender == 1:
        return 5
    else:
        return 4

@csrf_exempt
def clusterReport(request):
    if request.method == "GET":
        argsArray = []
        title = ""
        args = {"data": json.dumps(argsArray), "title": title}
        return render(request, "api/cluster.html", args)


@csrf_exempt
def pieChart(request, ageReport, smokeReport):
    if request.method == "GET":
        argsArray = []
        title = ""
        workersDict = Worker.objects.all()
        if int(ageReport) == 1:
            firstGroup = []
            secondGroup = []
            thirdGroup = []
            fourGroup = []
            fifthGroup = []
            for workerObject in workersDict:
                agePointValue = agePoint(int(workerObject.age))
                if agePointValue == 1:
                    firstGroup.append(workerObject)
                elif agePointValue == 2:
                    secondGroup.append(workerObject)
                elif agePointValue == 3:
                    thirdGroup.append(workerObject)
                elif agePointValue == 4:
                    fourGroup.append(workerObject)
                else:
                    fifthGroup.append(workerObject)
            universeAgeReport = len(firstGroup) + len(secondGroup) + len(thirdGroup) + len(fourGroup) + len(fifthGroup)
            argsArray.append({"label": "Entre 18 y 25", "y": float((len(firstGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "Entre 26 y 35", "y": float((len(secondGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "Entre 36 y 45", "y": float((len(thirdGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "Entre 46 y 55", "y": float((len(fourGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "56 en adelante", "y": float((len(fifthGroup)*100)/universeAgeReport)})
            title = "GRUPO DE EDAD"
        elif int(ageReport) == 2:
            workersDictRight = Worker.objects.filter(hand=1)
            workersDictLeft = Worker.objects.filter(hand=0)
            workersDictBoth = Worker.objects.filter(hand=2)
            universeAgeReport = len(workersDictRight) + len(workersDictLeft) + len(workersDictBoth)
            argsArray.append({"label": "Derecho", "y": float((len(workersDictRight)*100)/universeAgeReport)})
            argsArray.append({"label": "Izquierdo", "y": float((len(workersDictLeft)*100)/universeAgeReport)})
            argsArray.append({"label": "Ambos", "y": float((len(workersDictBoth)*100)/universeAgeReport)})
            title = "USTED ES"
        elif int(ageReport) == 3:
            firstGroup = []
            secondGroup = []
            thirdGroup = []
            fourGroup = []
            fifthGroup = []
            for workerObject in workersDict:
                imc = float(workerObject.weight) / float(workerObject.height)
                imcPointValue = imcPoint(round(imc,2))
                if imcPointValue == 1:
                    firstGroup.append(workerObject)
                elif imcPointValue == 2:
                    secondGroup.append(workerObject)
                elif imcPointValue == 3:
                    thirdGroup.append(workerObject)
                elif imcPointValue == 4:
                    fourGroup.append(workerObject)
                else:
                    fifthGroup.append(workerObject)
            universeAgeReport = len(firstGroup) + len(secondGroup) + len(thirdGroup) + len(fourGroup) + len(fifthGroup)
            argsArray.append({"label": "Rango normal: 18,5 - 24,9", "y": float((len(firstGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "Sobrepeso: 25 - 29,9", "y": float((len(secondGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "Obesidad grado I: 30 - 34,9", "y": float((len(thirdGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "Obesidad grado II: 35 - 39,9", "y": float((len(fourGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "Obesidad grado III > 40", "y": float((len(fifthGroup)*100)/universeAgeReport)})
            title = "CLASIFICACION IMC"
        elif int(ageReport) == 4:
            firstGroup = []
            secondGroup = []
            thirdGroup = []
            fourGroup = []
            fifthGroup = []
            for workerObject in workersDict:
                agePointValue = yearsPoint(int(workerObject.yearsCompany))
                if agePointValue == 1:
                    firstGroup.append(workerObject)
                elif agePointValue == 2:
                    secondGroup.append(workerObject)
                elif agePointValue == 3:
                    thirdGroup.append(workerObject)
                elif agePointValue == 4:
                    fourGroup.append(workerObject)
                else:
                    fifthGroup.append(workerObject)
            universeAgeReport = len(firstGroup) + len(secondGroup) + len(thirdGroup) + len(fourGroup) + len(fifthGroup)
            argsArray.append({"label": "Menor a un año", "y": float((len(firstGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "Entre 1 y 5 años", "y": float((len(secondGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "Entre 6 y 10 años", "y": float((len(thirdGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "Entre 11 y 15 años", "y": float((len(fourGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "16 años en adelante", "y": float((len(fifthGroup)*100)/universeAgeReport)})
            title = "GRUPO DE ANTIGUEDAD EN EL CARGO"
        elif int(ageReport) == 5:
            workersNoSmoke = Worker.objects.filter(smoke=1)
            workersYesSmoke = Worker.objects.filter(smoke=0)
            universeAgeReport = len(workersNoSmoke) + len(workersYesSmoke)
            argsArray.append({"label": "Si", "y": float((len(workersYesSmoke)*100)/universeAgeReport)})
            argsArray.append({"label": "No", "y": float((len(workersNoSmoke)*100)/universeAgeReport)})
            title = "FUMA"
        elif int(ageReport) == 6:
            firstGroup = []
            secondGroup = []
            thirdGroup = []
            for workerObject in workersDict:
                agePointValue = cigarrettesQuantityPoint(workerObject.how_much_cigarettes)
                if agePointValue == 3:
                    firstGroup.append(workerObject)
                elif agePointValue == 4:
                    secondGroup.append(workerObject)
                elif agePointValue == 5:
                    thirdGroup.append(workerObject)
            universeAgeReport = len(firstGroup) + len(secondGroup) + len(thirdGroup)
            argsArray.append({"label": "1 a 5 cigarrillos", "y": float((len(firstGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "6 a 15 cigarrillos", "y": float((len(secondGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "Más de 16 cigarrillos", "y": float((len(thirdGroup)*100)/universeAgeReport)})
            title = "CIGARRILLOS FUMADOS AL DIA"
        elif int(ageReport) == 7:
            firstGroup = []
            secondGroup = []
            thirdGroup = []
            fourGroup = []
            fifthGroup = []
            for workerObject in workersDict:
                agePointValue = howMuchSmokePoint(workerObject.how_much_smoke)
                if agePointValue == 1:
                    firstGroup.append(workerObject)
                elif agePointValue == 2:
                    secondGroup.append(workerObject)
                elif agePointValue == 3:
                    thirdGroup.append(workerObject)
                elif agePointValue == 4:
                    fourGroup.append(workerObject)
                else:
                    fifthGroup.append(workerObject)
            universeAgeReport = len(firstGroup) + len(secondGroup) + len(thirdGroup) + len(fourGroup) + len(fifthGroup)
            argsArray.append({"label": "Menos de un año", "y": float((len(firstGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "1 a 2 años", "y": float((len(secondGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "3 a 4 años", "y": float((len(thirdGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "5 a 9 años", "y": float((len(fourGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "10 años en adelante", "y": float((len(fifthGroup)*100)/universeAgeReport)})
            title = "HACE CUANTO TIEMPO FUMA"
        elif int(ageReport) == 8:
            workersNoSmoke = Worker.objects.filter(physical_activity_question=1)
            workersYesSmoke = Worker.objects.filter(physical_activity_question=0)
            universeAgeReport = len(workersNoSmoke) + len(workersYesSmoke)
            argsArray.append({"label": "Si", "y": float((len(workersYesSmoke)*100)/universeAgeReport)})
            argsArray.append({"label": "No", "y": float((len(workersNoSmoke)*100)/universeAgeReport)})
            title = "REALIZA ACTIVIDAD FISICA"
        elif int(ageReport) == 9:
            firstGroup = []
            secondGroup = []
            thirdGroup = []
            fourGroup = []
            for workerObject in workersDict:
                agePointValue = frequencyPhysicalActivityPoint(int(workerObject.frequency))
                if agePointValue == 5:
                    firstGroup.append(workerObject)
                elif agePointValue == 4:
                    secondGroup.append(workerObject)
                elif agePointValue == 3:
                    thirdGroup.append(workerObject)
                elif agePointValue == 2:
                    fourGroup.append(workerObject)

            universeAgeReport = len(firstGroup) + len(secondGroup) + len(thirdGroup) + len(fourGroup)
            argsArray.append({"label": "Diario", "y": float((len(firstGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "Dos veces a la semana", "y": float((len(secondGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "Tres veces a la semana", "y": float((len(thirdGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "Fines de semana", "y": float((len(fourGroup)*100)/universeAgeReport)})
            title = "FRECUENCIA ACTIVIDAD FISICA"
        elif int(ageReport) == 10:
            firstGroup = []
            secondGroup = []
            thirdGroup = []
            fourGroup = []
            for workerObject in workersDict:
                if workerObject.duration:
                    agePointValue = durationPhysicalActivityPoint(int(workerObject.duration))
                    if agePointValue == 1:
                        firstGroup.append(workerObject)
                    elif agePointValue == 2:
                        secondGroup.append(workerObject)
                    elif agePointValue == 3:
                        thirdGroup.append(workerObject)
                    elif agePointValue == 4:
                        fourGroup.append(workerObject)

            universeAgeReport = len(firstGroup) + len(secondGroup) + len(thirdGroup) + len(fourGroup)
            argsArray.append({"label": "15 minutos", "y": float((len(firstGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "30 minutos", "y": float((len(secondGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "1 hora", "y": float((len(thirdGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "Más de una hora", "y": float((len(fourGroup)*100)/universeAgeReport)})
            title = "DURACIÓN ACTIVIDAD FISICA"
        elif int(ageReport) == 11:
            firstGroup = []
            secondGroup = []
            thirdGroup = []
            fourGroup = []
            for workerObject in workersDict:
                if workerObject.how_much_hours_work:
                    agePointValue = workedHoursPoint(int(workerObject.how_much_hours_work))
                    if agePointValue == 2:
                        firstGroup.append(workerObject)
                    elif agePointValue == 3:
                        secondGroup.append(workerObject)
                    elif agePointValue == 4:
                        thirdGroup.append(workerObject)
                    elif agePointValue == 5:
                        fourGroup.append(workerObject)

            universeAgeReport = len(firstGroup) + len(secondGroup) + len(thirdGroup) + len(fourGroup)
            argsArray.append({"label": "1 a 4 horas", "y": float((len(firstGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "5 a 8 horas", "y": float((len(secondGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "8 a 12 horas", "y": float((len(thirdGroup)*100)/universeAgeReport)})
            argsArray.append({"label": "Más de 12 horas", "y": float((len(fourGroup)*100)/universeAgeReport)})
            title = "HORAS DIARIAS TRABAJADAS"
        elif int(ageReport) == 12:
            workersNoSmoke = Worker.objects.filter(vialbility_job_journey=1)
            workersYesSmoke = Worker.objects.filter(vialbility_job_journey=0)
            universeAgeReport = len(workersNoSmoke) + len(workersYesSmoke)
            argsArray.append({"label": "Si", "y": float((len(workersYesSmoke)*100)/universeAgeReport)})
            argsArray.append({"label": "No", "y": float((len(workersNoSmoke)*100)/universeAgeReport)})
            title = "DURACIÓN DE SU TRABAJO ES VARIABLE"
        elif int(ageReport) == 13:
            workersNoSmoke = Worker.objects.filter(inconvenience_body=1)
            workersYesSmoke = Worker.objects.filter(inconvenience_body=0)
            universeAgeReport = len(workersNoSmoke) + len(workersYesSmoke)
            argsArray.append({"label": "Si", "y": float((len(workersYesSmoke)*100)/universeAgeReport)})
            argsArray.append({"label": "No", "y": float((len(workersNoSmoke)*100)/universeAgeReport)})
            title = "PRESENTA DOLOR, MOLESTIA O DISCONFORT EN ALGUNA PARTE DEL CUERPO"
        elif int(ageReport) == 14:
            workersNoSmoke = Worker.objects.filter(sickness=1)
            workersYesSmoke = Worker.objects.filter(sickness=0)
            universeAgeReport = len(workersNoSmoke) + len(workersYesSmoke)
            argsArray.append({"label": "Si", "y": float((len(workersYesSmoke)*100)/universeAgeReport)})
            argsArray.append({"label": "No", "y": float((len(workersNoSmoke)*100)/universeAgeReport)})
            title = "PRESENTA ALGUNA ENFERMEDAD ACTUALMENTE"
        elif int(ageReport) == 15:
            workersNoSmoke = Worker.objects.filter(gender=1)
            workersYesSmoke = Worker.objects.filter(gender=0)
            universeAgeReport = len(workersNoSmoke) + len(workersYesSmoke)
            argsArray.append({"label": "Masculino", "y": float((len(workersYesSmoke)*100)/universeAgeReport)})
            argsArray.append({"label": "Femenino", "y": float((len(workersNoSmoke)*100)/universeAgeReport)})
            title = "SEXO"
        elif int(ageReport) == 16:
            for workerObject in workersDict:
                workersDictInside = Worker.objects.filter(name=workerObject.name)
                argsArray.append({"label": ""+workerObject.name+"", "y": float((len(workersDictInside)*100)/len(workersDict))})
            title = "NOMBRE"
        elif int(ageReport) == 17:
            for workerObject in workersDict:
                workersDictInside = Worker.objects.filter(lastname=workerObject.lastname)
                argsArray.append({"label": ""+workerObject.lastname+"", "y": float((len(workersDictInside)*100)/len(workersDict))})
            title = "APELLIDO"
        elif int(ageReport) == 18:
            for workerObject in workersDict:
                workersDictInside = Worker.objects.filter(identification=workerObject.identification)
                argsArray.append({"label": ""+workerObject.identification+"", "y": float((len(workersDictInside)*100)/len(workersDict))})
            title = "IDENTIFICACION"

        args = {"data": json.dumps(argsArray), "title": title}
        return render(request, "api/graphs.html", args)

@csrf_exempt
def login(request):
    if request.method == "POST":
        bodyUnicode = request.body.decode('utf-8')
        body = json.loads(bodyUnicode)
        userFind = authenticate(username=body['username'], password=body['password'])
        if userFind:
            usersCompanyDict = []
            usersCompany = Company.objects.filter(user=userFind)
            for companyObject in usersCompany:
                companyEmployees = Worker.objects.filter(company=companyObject)
                employeesDict = []
                if len(companyEmployees) != 0:
                    for employeeObject in companyEmployees:
                        employeesDict.append({"id": employeeObject.id, "name": employeeObject.name, "lastname": employeeObject.lastname,
                        "identification": employeeObject.identification, "weight": employeeObject.weight, "height": employeeObject.height,
                        "age": employeeObject.age, "gender": employeeObject.gender, "monthsCompany": employeeObject.monthsCompany,
                        "yearsCompany": employeeObject.yearsCompany, "dependency": employeeObject.dependency, "dominance": str(employeeObject.hand)})
                    usersCompanyDict.append({"employees": employeesDict,"id": companyObject.id, "name": companyObject.name, "nit": companyObject.nit, "city": companyObject.city, "department": companyObject.department, "date": str(companyObject.date)})
                else:
                    usersCompanyDict.append({"employees": employeesDict,"id": companyObject.id, "name": companyObject.name, "nit": companyObject.nit, "city": companyObject.city, "department": companyObject.department, "date": str(companyObject.date)})
            return HttpResponse(json.dumps({"status": "OK", "message": "", "id": userFind.id, "companies": usersCompanyDict}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "FALSE", "message": "Credenciales invalidas"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"error": "Invalid method"}), content_type="application/json")

@csrf_exempt
def addEmployee(request):
    if request.method == "POST":
        bodyUnicode = request.body.decode('utf-8')
        body = json.loads(bodyUnicode)
        employeeJsonObject = body["employee"]
        employeeToEdit = Worker()

        employeeToEdit.name = employeeJsonObject["name"]
        employeeToEdit.lastname = employeeJsonObject["lastname"]

        employeeToEdit.identification = employeeJsonObject["identification"]
        employeeToEdit.weight = employeeJsonObject["weight"]
        employeeToEdit.height = employeeJsonObject["height"]

        employeeToEdit.gender = int(employeeJsonObject["gender"])
        employeeToEdit.age = employeeJsonObject["age"]

        employeeToEdit.hand = int(employeeJsonObject["dominance"])
        employeeToEdit.monthsCompany = employeeJsonObject["monthsCompany"]
        employeeToEdit.yearsCompany = employeeJsonObject["yearsCompany"]
        employeeToEdit.dependency = employeeJsonObject["dependency"]

        employeeToEdit.company = Company.objects.get(id=employeeJsonObject["company"])

        employeeToEdit.smoke = employeeJsonObject["smoke"]
        employeeToEdit.how_much_cigarettes = employeeJsonObject["cigarretes"]
        employeeToEdit.how_much_smoke = employeeJsonObject["howLongSmoke"]
        employeeToEdit.physical_activity_question = employeeJsonObject["physicalActivity"]
        employeeToEdit.physical_activity = employeeJsonObject["physicalActivityName"]
        employeeToEdit.frequency = employeeJsonObject["frequency"]
        employeeToEdit.duration = employeeJsonObject["duration"]
        employeeToEdit.job_journey = employeeJsonObject["jobJourney"]
        employeeToEdit.vialbility_job_journey = employeeJsonObject["viabilityJobJourney"]
        employeeToEdit.how_much_hours_work = employeeJsonObject["workHoursByDay"]
        employeeToEdit.explanation_job_hours = employeeJsonObject["viabilityJobJourneyExplanation"]
        employeeToEdit.inconvenience_body = employeeJsonObject["inconveniences"]
        employeeToEdit.sickness = employeeJsonObject["sickness"]
        employeeToEdit.sick = employeeJsonObject["sickName"]
        employeeToEdit.sick_observations = employeeJsonObject["observations"]

        employeeToEdit.save()

        workerFormsDict = body["employeeForms"]
        filledFormObject = FilledForms()
        filledFormObject.worker = employeeToEdit
        filledFormObject.save()

        for workerFormObject in workerFormsDict:
            bodyPartFormObject = BodyPartForm()
            bodyPartFormObject.bodyPart = BodyPart.objects.get(id=workerFormObject["id"])
            bodyPartFormObject.paiSide = workerFormObject["id"]
            bodyPartFormObject.painWhen = workerFormObject["id"]
            bodyPartFormObject.painPresentedHow = workerFormObject["id"]
            bodyPartFormObject.painAgo = workerFormObject["id"]
            bodyPartFormObject.painDuration = workerFormObject["id"]
            bodyPartFormObject.painIntensity = workerFormObject["id"]
            bodyPartFormObject.painLevel = workerFormObject["id"]
            bodyPartFormObject.painLevelWork = workerFormObject["id"]
            bodyPartFormObject.save()
            filledFormObject.filledForms.add(bodyPartFormObject)

        filledFormObject.save()

        return HttpResponse(json.dumps({"status": "OK", "error": ""}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"status": "ERROR", "error": "Invalid method"}), content_type="application/json")

@csrf_exempt
def editEmployee(request):
    if request.method == "POST":
        bodyUnicode = request.body.decode('utf-8')
        body = json.loads(bodyUnicode)
        employeeToEdit = Worker.objects.get(id=body["id"])

        employeeToEdit.name = body["name"]
        employeeToEdit.lastname = body["lastname"]

        employeeToEdit.identification = body["identification"]
        employeeToEdit.weight = body["weight"]
        employeeToEdit.height = body["height"]

        employeeToEdit.gender = int(body["gender"])
        employeeToEdit.age = body["age"]

        employeeToEdit.hand = int(body["dominance"])
        employeeToEdit.monthsCompany = body["monthsCompany"]
        employeeToEdit.yearsCompany = body["yearsCompany"]
        employeeToEdit.dependency = body["dependency"]

        employeeToEdit.save()
        return HttpResponse(json.dumps({"status": "OK", "error": ""}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"status": "ERROR", "error": "Invalid method"}), content_type="application/json")

@csrf_exempt
def addCompany(request):
	if request.method == "POST":
		bodyUnicode = request.body.decode('utf-8')
		body = json.loads(bodyUnicode)
		constitutionDate = datetime.datetime.strptime(body["date"], "%d/%m/%Y").strftime("%Y-%m-%d")
		try:
			Company.objects.create(name=body["name"], nit=body["nit"], date=constitutionDate, city=body["city"], department=body["department"])
			return HttpResponse(json.dumps({"status": "OK", "message": ""}), content_type="application/json")
		except Exception:
			return HttpResponse(json.dumps({"status": "ERROR", "message": "La empresa ya se encuentra registrada"}), content_type="application/json")

	else:
		return HttpResponse(json.dumps({"error": "Invalid method"}), content_type="application/json")
