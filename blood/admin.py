from django.contrib import admin
from .models import *
from donor import models as dmodels
from patient import models as pmodels

# Register your models here.
admin.site.register(Stored)
admin.site.register(RequestBllod)
admin.site.register(pmodels.Patient)
admin.site.register(dmodels.Donor)