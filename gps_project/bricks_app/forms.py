from django import forms
from . models import CustomerMaster, DeviceMaster 

class AddCustomerForm(forms.ModelForm):
    Customer_Name = forms.CharField(label='Name', max_length=100, required=True)
    Customer_Phone = forms.CharField(label='Phone Number', max_length=20, required=True)
    Customer_Address = forms.CharField(label='Address', max_length=100, required=True)

    class Meta: 
        model = CustomerMaster
        exclude = ['Customer_Id', 'Customer_Status']


class AddDeviceForm(forms.ModelForm):
    Customers_Details = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Customer Details',
            'autocomplete': 'off'
        })
    )

    class Meta:
        model = DeviceMaster
        fields = [
            'Customers_Details',
            'Gps_Imei_No', 'Model', 'Sim_No',
            'Vehicle_No', 'Vehicle_Name',
            'Insurance_Name', 'Insurance_End_Date', 'Next_Renewal_Date'
        ]
        widgets = {
            'Gps_Imei_No': forms.TextInput(attrs={'placeholder': 'Enter GPS IMEI No'}),
            'Model': forms.TextInput(attrs={'placeholder': 'Enter Model'}),
            'Sim_No': forms.TextInput(attrs={'placeholder': 'Enter SIM No'}),
            'Vehicle_No': forms.TextInput(attrs={'placeholder': 'Enter Vehicle No'}),
            'Vehicle_Name': forms.TextInput(attrs={'placeholder': 'Enter Vehicle Name'}),
            'Insurance_Name': forms.TextInput(attrs={'placeholder': 'Enter Insurance Name'}),
            'Insurance_End_Date': forms.DateInput(attrs={'type': 'date'}),
            'Next_Renewal_Date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_Customers_Details(self):
        value = self.cleaned_data.get('Customers_Details', '').strip()

        try:
            customer_id, customer_name, customer_phone, customer_address = [x.strip() for x in value.split('---')]
        except ValueError:
            raise forms.ValidationError("Invalid format. Use: ID --- Name --- Phone --- Address")

        if not customer_phone.isdigit():
            raise forms.ValidationError("Phone must be numeric.")

        self.cleaned_data['Customer_Id'] = customer_id
        self.cleaned_data['Customer_Name'] = customer_name
        self.cleaned_data['Customer_Phone'] = int(customer_phone)
        self.cleaned_data['Customer_Address'] = customer_address

        return value


