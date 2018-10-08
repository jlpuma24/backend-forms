from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, Http404
from django.contrib.auth import authenticate
from api.models import *
import datetime
import json

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

        smoke = employeeJsonObject["smoke"]
        how_much_cigarettes = employeeJsonObject["cigarretes"]
        how_much_smoke = employeeJsonObject["howLongSmoke"]
        physical_activity_question = employeeJsonObject["physicalActivity"]
        physical_activity = employeeJsonObject["physicalActivityName"]
        frequency = employeeJsonObject["frequency"]
        duration = employeeJsonObject["duration"]
        job_journey = employeeJsonObject["jobJourney"]
        vialbility_job_journey = employeeJsonObject["viabilityJobJourney"]
        how_much_hours_work = employeeJsonObject["workHoursByDay"]
        explanation_job_hours = employeeJsonObject["viabilityJobJourneyExplanation"]
        inconvenience_body = employeeJsonObject["inconveniences"]
        sickness = employeeJsonObject["sickness"]
        sick = employeeJsonObject["sickName"]
        sick_observations = employeeJsonObject["observations"]

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
