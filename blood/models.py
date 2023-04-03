from django.db import models
from donor import models as dmodels
from patient import models as pmodels

# Create your models here.
class Stored(models.Model):
    blood_type = models.CharField(max_length=50)
    unites_number = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.blood_type


class RequestBllod(models.Model):
    donner_request = models.ForeignKey(dmodels.Donor, on_delete=models.CASCADE, null = True)
    patient_request = models.ForeignKey(pmodels.Patient, on_delete=models.CASCADE, null = True) 
    pat_name =  models.CharField(max_length=50)
    pat_age = models.PositiveIntegerField()
    blood_type = models.CharField(max_length=50)
    unites_number = models.PositiveIntegerField(default=0)
    purpose = models.CharField(max_length=300)
    status = models.CharField(max_length=40 , default="Pending")
    date_req =models.DateField(auto_now=True)
    def __str__(self):
        return self.blood_type
        
    
       
    
