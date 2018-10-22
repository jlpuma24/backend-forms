from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, Http404
from django.contrib.auth import authenticate
from api.models import *
import datetime
import json

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
    else:
        return 3

def workedHoursPoint(workedHours):
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
    elif age >= 26 and age <= 45:
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
def pieChart(request):
    if request.method == "GET":
        args = []
        return render(request, "api/graps.html", args)

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
