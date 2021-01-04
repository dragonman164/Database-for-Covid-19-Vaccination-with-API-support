"""databaseforvaccination URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url,include
from .views import index,license,table,PersonList,ReportList,ManagementList,Person_without_aadhar_viewer
from rest_framework.routers import DefaultRouter




urlpatterns = [
    path('',index,name="Index"),
    path('license/',license,name="license"),
    path('table/',table,name="table"),
    path('api/',PersonList.as_view(),name="API"),
    path('api1/',ReportList.as_view(),name="API1"),
    path('api2/',ManagementList.as_view(),name="API2"),
    url('api3/',Person_without_aadhar_viewer.as_view(),name="API3"),
    # path('api3/',Person_without_aadhar_viewer,name="API3")

]
