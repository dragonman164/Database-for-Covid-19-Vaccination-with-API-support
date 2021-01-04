from django.http import response
from django.shortcuts import render,HttpResponse
from .models import Person,report,management,Person_without_Aadhar
import datetime
from django.utils.timezone import utc
from rest_framework import serializers, status,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser,FormParser
from .serializers import PersonSerializer,ReportSerializer,ManagementSerializer,Person_Without_Aadhar_Serializer
from functools import cmp_to_key
import face_recognition
import os




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
            serializer.save()
            noofvaccinesperday = 2
            days = 0
            curr_date = datetime.date.today()
            obj = Person.objects.all()
            
            current_zone = set()
            zone_wise_data = {}
            for elem in obj:
                if not elem.isVaccinated:
                    current_zone.add(f'{elem.area} + {elem.zone}')
            
            for zones in current_zone:
                zone_wise_data[zones] = []

            for elem in obj:
                if not elem.isVaccinated:
                    zone_wise_data[f'{elem.area} + {elem.zone}'].append(elem)
        
        
            for elem in zone_wise_data.values():
                days = 0
                for person in elem:
                    if person.dateofvaccination == None or person.dateofvaccination <  curr_date:
                        person.dateofvaccination = curr_date
                    days+=1
                    if days == noofvaccinesperday:
                        days = 0
                        curr_date += datetime.timedelta(1)
                    person.save()


            data1["success"] = "Update Successful"
            return Response(data1,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)


class ReportList(APIView):
    
    def get(self,request,*args,**kwargs):
        obj = report.objects.all()
        serializer = ReportSerializer(obj,many=True)
        return Response(serializer.data)
    
    def post(self,request,*args,**kwargs):
        serializer = ReportSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)


class ManagementList(APIView):
    
    def get(self,request,*args,**kwargs):
        obj = management.objects.all()
        serializer = ManagementSerializer(obj,many=True)
        return Response(serializer.data)
    
    def post(self,request,*args,**kwargs):
        serializer = ManagementSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)   


class Person_without_aadhar_viewer(APIView):
    parser_class = (MultiPartParser,FormParser)
    queryset = Person_without_Aadhar.objects.all()
    serializer_class = Person_Without_Aadhar_Serializer



    def get(self, request,*args,**kwargs):

        obj = Person_without_Aadhar.objects.all()
        serializer = Person_Without_Aadhar_Serializer(obj,many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

      serializer = Person_Without_Aadhar_Serializer(data=request.data)
      

      if serializer.is_valid():
        file_name = request.data['file']
        image_files = os.listdir('media/')
        instance = serializer.save()
        if len(image_files) != 0:
            imagedata = []
            for image in image_files:
                if image != file_name:
                    get_image = face_recognition.load_image_file(f"media/{image}")
                    imagedata.append(face_recognition.face_encodings(get_image)[0])
            
            unknown_image = face_recognition.load_image_file(f'media/{file_name}')
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        

            for image in imagedata:
                results = face_recognition.compare_faces([image],unknown_encoding)
                if results[0] == True:
                    instance.delete()
                    return Response({'Error':'This Person is in this database'})
        
        noofvaccinesperday = 2
        days = 0
        curr_date = datetime.date.today()
        obj = Person_without_Aadhar.objects.all()
        current_zone = set()
        zone_wise_data = {}
        for elem in obj:
            if not elem.isVaccinated:
                current_zone.add(f'{elem.area} + {elem.zone}')
        
        for zones in current_zone:
            zone_wise_data[zones] = []

        for elem in obj:
            if not elem.isVaccinated:
                zone_wise_data[f'{elem.area} + {elem.zone}'].append(elem)
    
    
        for elem in zone_wise_data.values():
            days = 0
            for person in elem:
                if person.dateofvaccination == None or person.dateofvaccination <  curr_date:
                    person.dateofvaccination = curr_date
                days+=1
                if days == noofvaccinesperday:
                    days = 0
                    curr_date += datetime.timedelta(1)
                person.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      else:

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    obj3 = Person_without_Aadhar.objects.all()
    params = {
        'Database': obj,
        'Database1': obj1,
        'Database2': obj2,
        'Database3':obj3,
        'time': datetime.datetime.utcnow().replace(tzinfo=utc),
    }
    return render(request,"maindatabase/tables.html",params)