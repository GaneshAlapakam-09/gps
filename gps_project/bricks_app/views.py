import base64
import datetime
import io
import json
from django.http import JsonResponse
from django.shortcuts import render ,redirect
from . models import CustomerMaster,DeviceMaster
from . forms import AddCustomerForm, AddDeviceForm
from datetime import date
from django.contrib import messages
from django.shortcuts import get_object_or_404 

def dashboard(request):
      return render(request,'index.html')

def add_customer(request):
    form=AddCustomerForm()
    last_customer = CustomerMaster.objects.order_by('-Customer_Id').first()
    if last_customer:
        last_id = int(last_customer.Customer_Id[4:])  # Extract the numeric part
        new_id = f"CUST{last_id + 1:04d}"         
    else:
        new_id = "CUST0001"

    if request.method=='POST':
        form=AddCustomerForm(request.POST)
        print("data sent Post forms.py")
        if form.is_valid():
            print("data valid")
            customer = CustomerMaster()
            customer.Customer_Id = new_id
            customer.Customer_Status = 1
            customer.Customer_Name = form.cleaned_data['Customer_Name']
            customer.Customer_Phone = form.cleaned_data['Customer_Phone']
            customer.Customer_Address = form.cleaned_data['Customer_Address']
            customer.save()
            print("data saved success")
            messages.success(request,"Add customer successfully")
            return redirect('add_customer')

    return render(request,"add_customer.html",{'form':form,'new_id':new_id})
       
def list_customer(request):
    customer_data=CustomerMaster.objects.filter(Customer_Status=1)
    return render(request,'list_customer.html',{'customer_data':customer_data})


def add_device(request):
    if request.method == 'POST':
        form = AddDeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)

            # Get parsed customer fields
            device.Customer_Id = form.cleaned_data['Customer_Id']
            device.Customer_Name = form.cleaned_data['Customer_Name']
            device.Customer_Phone = form.cleaned_data['Customer_Phone']
            device.Customer_Address = form.cleaned_data['Customer_Address']

            device.save()
            messages.success(request, "Device added successfully.")

            return redirect('add_device')
    else:
        form = AddDeviceForm()
    customer_data=CustomerMaster.objects.filter(Customer_Status=1)
    
    return render(request,'add_device.html',{'sent': customer_data,'form':form})

def list_device(request):
    device_data=DeviceMaster.objects.all()
    return render(request,'list_device.html',{'sent':device_data})

       
       

