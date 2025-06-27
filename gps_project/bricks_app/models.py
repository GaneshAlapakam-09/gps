from django.db import models


class CustomerMaster(models.Model):
    Customer_Id = models.CharField(max_length=20, unique=True)
    Customer_Name = models.CharField(max_length=100)
    Customer_Phone = models.BigIntegerField()
    Customer_Address = models.CharField(max_length=200)

    
    Customer_Status = models.IntegerField(default=1)

    def __str__(self):
        return self.Customer_Name

    

class DeviceMaster(models.Model):
    #customer details
    Customer_Id=models.CharField(max_length=20)
    Customer_Name=models.CharField(max_length=255)
    Customer_Phone=models.BigIntegerField()
    Customer_Address=models.CharField(max_length=200)

    Gps_Imei_No=models.CharField(max_length=200)
    Model=models.CharField(max_length=200)
    Sim_No=models.CharField(max_length=200)
    Vehicle_No=models.CharField(max_length=200)
    Vehicle_Name=models.CharField(max_length=200)
    Insurance_Name=models.CharField(max_length=200)
    Insurance_End_Date = models.DateField(null=True, auto_now=False, auto_now_add=False)
    Next_Renewal_Date = models.DateField(null=True, auto_now=False, auto_now_add=False)


    def __str__(self):
        return self.Customer_Name
    
