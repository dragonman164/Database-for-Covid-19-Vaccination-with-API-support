from django.shortcuts import render,HttpResponse
from .models import Person,report,management
import datetime
from django.utils.timezone import utc
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PersonSerializer
from functools import cmp_to_key



def comparator(a,b):
    if a.occupation not in ['Doctor','Nurse','Police'] and b.occupation in ['Doctor','Nurse','Police']:
        return 1
    elif a.occupation in ['Doctor','Nurse','Police'] and b.occupation not in ['Doctor','Nurse','Police']:
        return -1
    elif a.occupation in ['Doctor','Nurse','Police'] and b.occupation in ['Doctor','Nurse','Police']:
        if not a.isatRisk and b.isatRisk:
            return 1
        elif a.isatRisk and not b.isatRisk:
            return -1
        elif not a.age >= 60 and  b.age>=60:
            return 1
        elif a.age>=60 and not b.age>=60:
            return -1
        else:
            return 0
    elif not a.isatRisk and b.isatRisk:
            return 1
    elif a.isatRisk and not b.isatRisk:
        return -1
    elif not a.age >= 60 and  b.age>=60:
        return 1
    elif a.age>=60 and not b.age>=60:
        return -1
    return 0


class PersonList(APIView):
    def get(self,request,*args,**kwargs):
        obj = Person.objects.all()
        serializer = PersonSerializer(obj,many=True)
        return Response(serializer.data)

    def put(self,request,*args,**kwargs):
        


        serializer = PersonSerializer(data = request.data)
        obj = Person.objects.filter(pk= request.data['aadhar_number'])
        print(obj)
        obj.delete()
        data1 = {}
        if serializer.is_valid():
            print("Hello World")
            serializer.save()

            tobeVaccinated = []
            noofvaccinesperday = 2
            days = 0
            curr_date = datetime.date.today()
            obj = Person.objects.all()
            
            for elem in obj:
                if not elem.isVaccinated:
                    tobeVaccinated.append(elem)
            data = sorted(tobeVaccinated,key=cmp_to_key(comparator))
        
            for elem in data:
                if elem.dateofvaccination == None or elem.dateofvaccination <  curr_date:
                    elem.dateofvaccination = curr_date
                days+=1
                if days == noofvaccinesperday:
                    days = 0
                    curr_date += datetime.timedelta(1)
                elem.save()


            data1["success"] = "Update Successful"
            return Response(data1,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    # def post(self,request):
    #     serializer = PersonSerializer(data = request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data,status= status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Create your views here.
def index(request):
    count = 0
    obj = Person.objects.all()
    for elem in obj:
        if elem.isVaccinated:
            count+=1
    
    params = {
        'Total' : len(obj),
        'Vaccinated':count,
        'TobeVaccinated':len(obj)-count
    }

    return render(request,"maindatabase/index.html",params)

def license(request):
    return render(request,"maindatabase/license.html")

def table(request):
    obj = Person.objects.all()
    obj1 = report.objects.all()
    obj2 = management.objects.all()
    params = {
        'Database': obj,
        'Database1': obj1,
        'Database2': obj2,
        'time': datetime.datetime.utcnow().replace(tzinfo=utc),
    }
    return render(request,"maindatabase/tables.html",params)