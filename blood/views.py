from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import Group
from django.db.models import Sum,Q
from django.conf import settings
from donor import models as dmodels
from patient import forms as pforms
from patient import models as pmodels
from . import models, forms
from django.contrib.auth import authenticate, login, logout
from donor import forms as dforms
from django.contrib.auth.models import User
# Create your views here.
def home_dashbored(request):
    # store the name of blood group in db 
    x=models.Stored.objects.all()
    print(x)
    if len(x)==0:
        blood1=models.Stored()
        blood1.bloodgroup="A+"
        blood1.save()

        blood2=models.Stored()
        blood2.bloodgroup="A-"
        blood2.save()

        blood3=models.Stored()
        blood3.bloodgroup="B+"
        blood3.save()        

        blood4=models.Stored()
        blood4.bloodgroup="B-"
        blood4.save()

        blood5=models.Stored()
        blood5.bloodgroup="AB+"
        blood5.save()

        blood6=models.Stored()
        blood6.bloodgroup="AB-"
        blood6.save()

        blood7=models.Stored()
        blood7.bloodgroup="O+"
        blood7.save()

        blood8=models.Stored()
        blood8.bloodgroup="O-"
        blood8.save()

    
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin') 
    return render(request,'blood/index.html')


def is_doner(user):
    return user.groups.filter(name='DONOR').exists()   #  checking if a user is member of certain group

def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()

def after_loginView(request):
    if is_doner(request.user):
        return redirect('donor/donor-dashboard')
    elif is_patient(request.user):
        return redirect('patient/patient-dashboard')
    else:
        return redirect('admin-dashboard')    

@login_required(login_url='/adminlogin/')
def admin_dashboard_view(request):
    # Sumation of total unit of blood from db
    totalunit=models.Stored.objects.aggregate(Sum('unites_number')) # aggregate(),you can make sum,avg,min,max from queryset
    dict={

        'A1':models.Stored.objects.get(blood_type="A+"),
        'A2':models.Stored.objects.get(blood_type="A-"),
        'B1':models.Stored.objects.get(blood_type="B+"),
        'B2':models.Stored.objects.get(blood_type="B-"),
        'AB1':models.Stored.objects.get(blood_type="AB+"),
        'AB2':models.Stored.objects.get(blood_type="AB-"),
        'O1':models.Stored.objects.get(blood_type="O+"),
        'O2':models.Stored.objects.get(blood_type="O-"),
        'totaldonors':dmodels.Donor.objects.all().count(),
        'totalbloodunit':totalunit['unites_number__sum'], # Sum('unites_number') -> unites_number__sum
        'totalrequest':models.RequestBllod.objects.all().count(),
        'totalapprovedrequest':models.RequestBllod.objects.all().filter(status='Approved').count()
    }
    return render(request,'blood/admin_dashboard.html', context=dict)

def Logout(request):
        logout(request)
        return redirect ("/")

@login_required(login_url='adminlogin')
def admin_blood_view(request):
    dict={
        'bloodForm':forms.BloodForm(),
        'A1':models.Stored.objects.get(blood_type="A+"),
        'A2':models.Stored.objects.get(blood_type="A-"),
        'B1':models.Stored.objects.get(blood_type="B+"),
        'B2':models.Stored.objects.get(blood_type="B-"),
        'AB1':models.Stored.objects.get(blood_type="AB+"),
        'AB2':models.Stored.objects.get(blood_type="AB-"),
        'O1':models.Stored.objects.get(blood_type="O+"),
        'O2':models.Stored.objects.get(blood_type="O-"),
    }
    if request.method=='POST':
        bloodForm=forms.BloodForm(request.POST)
        if bloodForm.is_valid() :        
            blood_type=bloodForm.cleaned_data['blood_type'] # override
            stock=models.Stored.objects.get(blood_type=blood_type)
            stock.unites_number=bloodForm.cleaned_data['unites_number'] # ov
            stock.save()
        return HttpResponseRedirect('admin-blood')
    return render(request,'blood/admin_blood.html',context=dict)        

@login_required(login_url='adminlogin')
def admin_donor_view(request):
    donors=dmodels.Donor.objects.all()
    return render(request,'blood/admin_donor.html',{'donors':donors})

@login_required(login_url='adminlogin')
def admin_patient_view(request):
    patients=pmodels.Patient.objects.all()
    return render(request,'blood/admin_patient.html',{'patients':patients})


@login_required(login_url='adminlogin')
def admin_donation_view(request):
    donations=dmodels.BloodDonate.objects.all()
    return render(request,'blood/admin_donation.html',{'donations':donations})    



@login_required(login_url='adminlogin')
def admin_request_history_view(request):
    requests=models.RequestBllod.objects.all().exclude(status='Pending')
    return render(request,'blood/admin_request_history.html',{'requests':requests})
    
@login_required(login_url='adminlogin')
def admin_request_view(request):
    requests=models.RequestBllod.objects.all().filter(status='Pending')
    return render(request,'blood/admin_request.html',{'requests':requests})    




@login_required(login_url='adminlogin')
def delete_donor_view(request,pk):
    donor=dmodels.Donor.objects.get(id=pk)
    user=User.objects.get(id=donor.user_id)
    user.delete()
    donor.delete()
    return HttpResponseRedirect('/admin-donor')
    

@login_required(login_url='adminlogin')
def delete_patient_view(request,pk):
    patient=pmodels.Patient.objects.get(id=pk)
    user=User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return HttpResponseRedirect('/admin-patient')    

@login_required(login_url='adminlogin')
def approve_donation_view(request,pk):
    donation=dmodels.BloodDonate.objects.get(id=pk)
    donation_blood_group=donation.bloodgroup
    donation_blood_unit=donation.unit

    stock=models.Stored.objects.get(blood_type=donation_blood_group)
    stock.unites_number=stock.unites_number+donation_blood_unit
    stock.save()

    donation.status='Approved'
    donation.save()
    return HttpResponseRedirect('/admin-donation')


@login_required(login_url='adminlogin')
def reject_donation_view(request,pk):
    donation=dmodels.BloodDonate.objects.get(id=pk)
    donation.status='Rejected'
    donation.save()
    return HttpResponseRedirect('/admin-donation')



@login_required(login_url='adminlogin')
def update_approve_status_view(request,pk):
    req=models.RequestBllod.objects.get(id=pk)
    message=None
    blood_type=req.blood_type
    unites_number=req.unites_number
    stock=models.Stored.objects.get(blood_type=blood_type)
    if stock.unites_number > unites_number:
        stock.unites_number=stock.unites_number-unites_number
        stock.save()
        req.status="Approved"
        
    else:
        message="Stock Doest Not Have Enough Blood To Approve This Request, Only "+str(stock.unites_number)+" Unit Available"
    req.save()

    requests=models.RequestBllod.objects.all().filter(status='Pending')
    return render(request,'blood/admin_request.html',{'requests':requests,'message':message})

@login_required(login_url='adminlogin')
def update_reject_status_view(request,pk):
    req=models.RequestBllod.objects.get(id=pk)
    req.status="Rejected"
    req.save()
    return HttpResponseRedirect('/admin-request')
