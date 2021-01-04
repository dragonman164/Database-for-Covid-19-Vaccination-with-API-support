from rest_framework import serializers
from rest_framework.fields import FileField
from . models import Person,report,management,Person_without_Aadhar


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
class ReportSerializer(serializers.ModelSerializer):        
    class Meta:
        model = report
        fields = '__all__'
class ManagementSerializer(serializers.ModelSerializer):        
    class Meta:
        model = management
        fields = '__all__'    

class Person_Without_Aadhar_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Person_without_Aadhar
        fields = '__all__'
          