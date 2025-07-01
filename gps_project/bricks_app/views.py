import base64
import datetime
import io
import json
from django.http import JsonResponse
from django.shortcuts import render ,redirect
from . models import CustomerMaster,DeviceMaster, OrderItem, Product, Order
from . forms import AddCustomerForm, AddDeviceForm
from datetime import date
from django.contrib import messages
from django.shortcuts import get_object_or_404 
from django.utils.timezone import localtime
from django.utils.dateparse import parse_datetime

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                return JsonResponse({
                    'success': True,
                    'role': "admin",  # Assuming `role` is a field on User model
                    # 'role': "employee",  # Assuming `role` is a field on User model
                    'token': 'dummy-token-or-jwt'  # You can replace with real token logic
                })
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'error': 'Only POST allowed'})


@csrf_exempt
def list_products(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            name = data.get('name')
            category = data.get('category')
            price = data.get('price')


            if not name or not category or price is None:
                return JsonResponse({'success': False, 'message': 'All fields are required'}, status=400)

            # Optional: Validate category
            # valid_categories = [c[0] for c in Product.CATEGORY_CHOICES]
            # if category.lower() not in valid_categories:
            #     return JsonResponse({'success': False, 'message': 'Invalid category'}, status=400)

            product = Product.objects.create(
                name=name,
                category=category.lower(),
                price=price,
                is_available=True
            )

            return JsonResponse({'success': True, 'message': 'Product added', 'product_id': product.id})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    if request.method == 'GET':
        category = request.GET.get('category')  # optional filter
        products = Product.objects.filter(is_available=True)
        
        if category:
            products = products.filter(category=category.lower())

        data = list(products.values('id', 'name', 'category', 'price'))
        return JsonResponse(data, safe=False)

    return JsonResponse({'error': 'Only GET method allowed'}, status=405)



@csrf_exempt
def list_orders(request):
    if request.method == 'GET':
        orders = Order.objects.all().order_by('-timestamp')
        data = [
            {
                "id": order.id,
                "date": localtime(order.timestamp).strftime("%Y-%m-%d %H:%M"),
                "total_amount": float(order.total),
                "payment_mode": order.payment_mode
            }
            for order in orders
        ]
        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def submit_order(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
        total = data.get('total')
        payment_mode = data.get('payment_mode')
        timestamp = parse_datetime(data.get('timestamp'))
        items = data.get('items', [])

        if not items:
            return JsonResponse({'error': 'No items in order'}, status=400)

        order = Order.objects.create(total=total, payment_mode=payment_mode, timestamp=timestamp)

        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(order=order, product=product, quantity=quantity)

        return JsonResponse({'message': 'Order created successfully', 'order_id': order.id})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)