from django import forms

from . import models


class BloodForm(forms.ModelForm):
    class Meta:
        model=models.Stored
        fields=['blood_type','unites_number']

class RequestForm(forms.ModelForm):
    class Meta:
        model=models.RequestBllod
        fields=['pat_name','pat_age','purpose','blood_type','unites_number']
