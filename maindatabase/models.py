from django.db import models
from datetime import datetime

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
    #AEFI_AESI_report
class report(models.Model):     
    MY_CHOICES = (
        ('None', 'None'),
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )
    name = models.CharField(max_length=200,null=False)
    aadhar_number = models.IntegerField(null=False,primary_key=True)
    age = models.IntegerField(null = False)
    description = models.CharField(max_length=1000,null=False)
    Fever = models.BooleanField(default=False)
    Pain_Severity = models.CharField(max_length=200,choices=MY_CHOICES)
    Any_allergies = models.BooleanField(default=False)

    #logistic management of vaccineclass
class management(models.Model):
    MY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )
    date_time = models.DateTimeField(auto_now=True)
    No_vaccine_dispatched = models.IntegerField(null=False)
    No_usable_vaccine = models.IntegerField(null=False)
    Temperature = models.IntegerField(null=False)
    Humidity = models.IntegerField(null=False)
    traffic_density=models.CharField(max_length=200,choices=MY_CHOICES)

