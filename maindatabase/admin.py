from django.contrib import admin
from .models import Person,report,management,Person_without_Aadhar

admin.site.register(Person)
admin.site.register(report)
admin.site.register(management)
admin.site.register(Person_without_Aadhar)
# Register your models here.
