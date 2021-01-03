from rest_framework import serializers
from . models import Person,report,management

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
          