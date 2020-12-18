from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=200,null=False)
    aadhar_number = models.IntegerField(null=False,primary_key=True)
    area = models.CharField(max_length=200,null=False)
    zone = models.CharField(max_length=200,null=False)
    age = models.IntegerField(null = False)
    occupation = models.CharField(max_length=200,default="None")
    isatRisk = models.BooleanField(default=False)
    dateofvaccination = models.DateField(blank=True,null=True)
    isVaccinated = models.BooleanField(default=False)


