# Create your models here.
from distutils.command.upload import upload
from email.policy import default
from statistics import mode
from tkinter import Image
from django.contrib.auth.models import User
from django.db import models

from django.db.models.fields.related import ForeignKey  
# Create your models here.

CATEGORY_CHOICES = (
  ('VENDOR','Vendor'),
  ('CUSTOMER','Customer'),
)

class UserProfile(models.Model):
    UserID=models.ForeignKey(User,on_delete=models.CASCADE)
    Image=models.ImageField(upload_to="images/",default='images/5f3bc92f9aec61bd99062249a9a87178.png')
    EntryDate = models.DateTimeField(auto_now=True)
    def __str__(self):
      return str(self.id)

class UserType(models.Model):
    UserID=models.ForeignKey(User,on_delete=models.CASCADE)
    UserType=models.CharField(max_length=100, choices=CATEGORY_CHOICES,blank=False)
    EntryDate = models.DateTimeField(auto_now=True)
    def __str__(self):
      return str(self.id)
    
STATUS_CHOICES = (
  ('PENDING','Pending'),
  ('APPROVED','Approved'),
  ('REJECTED','Rejected'),
)

class Restuarant(models.Model):
    RestuarantID= models.ForeignKey(User,on_delete=models.CASCADE)
    RestuarantName= models.CharField(max_length=100,unique=True)
    RestuarantCity =models.CharField(max_length=100,unique=False)
    RestuarantState= models.CharField(max_length=100,unique=False)
    RestuarantCountry=models.CharField(max_length=100,unique=False)
    Status=models.CharField(max_length=100, choices=STATUS_CHOICES,blank=False,default="Pending")
    def __str__(self):
      return str(self.RestuarantID)

class WebResources(models.Model):
   RestuarantID= models.ForeignKey(Restuarant,on_delete=models.CASCADE)
   Image     = models.ImageField(upload_to="images/")
   IDfront   = models.ImageField(upload_to="images/")
   IDblack   = models.ImageField(upload_to="images/")
   Location  = models.CharField(max_length=250,blank=True)
   Phone1    = models.CharField(max_length=13,unique=False)
   Phone2    = models.CharField(max_length=13,unique=False,blank=True)
   Day       = models.CharField(max_length=150,blank=True,null=True)
   OpeningTime = models.TimeField(blank=True,null=True)
   ClosingTime = models.TimeField(blank=True,null=True)
   LinkedInLink = models.CharField(max_length=100,blank=True,null=True)
   GitLink = models.CharField(max_length=100,blank=True,null=True)
   TwitterLink = models.CharField(max_length=100,blank=True,null=True)
   FbLink = models.CharField(max_length=100,blank=True,null=True)
   EntryDate = models.DateTimeField(auto_now=True)
   def __str__(self):
      return str(self.id)



STATUS_BILL = (
  ('PAID','Paid'),
  ('REQUESTED','Requested'),
  ('PENDING','Pending'),
)

class Billing(models.Model):
    RestuarantID= models.ForeignKey(Restuarant,on_delete=models.CASCADE)
    Status = models.CharField(max_length=30,choices=STATUS_BILL)
    Amount = models.FloatField()
    DateFrom = models.DateTimeField()
    DateTo = models.DateTimeField()
    EntryDate = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)

class CompletedPayments(models.Model):
    RestuarantID= models.ForeignKey(Restuarant,on_delete=models.CASCADE)
    Status = models.CharField(max_length=30)
    Amount = models.FloatField()
    DateFrom = models.DateTimeField()
    DateTo = models.DateTimeField()
    EntryDate = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)

class BankAccount(models.Model):
    BillingID=models.ForeignKey(Billing,on_delete=models.CASCADE)
    TransactionID=models.CharField(max_length=50)
    BankName=models.CharField(max_length=100)
    AccountNumber=models.CharField(max_length=50)
    CustomerName=models.CharField(max_length=50)
    EntryDate = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)


class Manager(models.Model):
    RestuarantID= models.ForeignKey(Restuarant,on_delete=models.CASCADE)
    Image     = models.ImageField(upload_to="images/")
    Name      = models.CharField(max_length=30)
    Rank      = models.CharField(max_length=50)
    EntryDate = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)

class Feeds(models.Model):
    RestuarantID = models.ForeignKey(Restuarant,on_delete=models.CASCADE)
    Username    = models.CharField(max_length=50)
    Email     = models.CharField(max_length=50)
    Comment   = models.CharField(max_length=250)
    EntryDate = models.DateTimeField(auto_now=True)
    def __str__(self):
       return str(self.id)

class Employee(models.Model):
    RestuarantID = models.ForeignKey(Restuarant,on_delete=models.CASCADE)
    FirstName     = models.CharField(max_length=30)
    LastName      = models.CharField(max_length=30,blank=True)
    CNIC          = models.CharField(max_length=13,unique=True,blank=True)
    FatherName    = models.CharField(max_length=30)
    Age           = models.IntegerField()
    Gender        = models.CharField(max_length=8)
    EntryDate     = models.DateTimeField(auto_now=True)
    def __str__(self):
       return str(self.id)

class Delivery(models.Model):
    RestuarantID    = models.ForeignKey(Restuarant,on_delete=models.CASCADE)
    EmployeePID     = models.ForeignKey(Employee,on_delete=models.CASCADE)
    CustomerOrderID = models.ForeignKey(User, on_delete=models.CASCADE) 
    DeliveryAddress = models.CharField(max_length=100)
    ExpectedTime    = models.CharField(max_length=10)
    EntryDate       = models.DateTimeField(auto_now=True)
    def __str__(self):
       return str(self.id)


class Product(models.Model):
    RestuarantID    = models.ForeignKey(Restuarant,on_delete=models.CASCADE)
    Foodname  = models.CharField(max_length=100) 
    Foodsize  = models.CharField(max_length=100) 
    Foodprice = models.CharField(max_length=100) 
    Fooddescription=models.CharField(max_length=100) 
    Foodimage = models.ImageField(upload_to='images/')
    EntryDate = models.DateTimeField(auto_now=True)
    def __str__(self):
       return str(self.id)

class Offers(models.Model):
    RestuarantID = models.ForeignKey(Restuarant,on_delete=models.CASCADE)
    OfferName    = models.CharField(max_length=30,unique=True)
    OfferItems   = models.CharField(max_length=250,unique=True)
    OfferPrice   = models.DecimalField(max_digits=8, decimal_places=2) 
    OfferDescription=models.CharField(max_length=250,unique=True)
    Availability = models.CharField(max_length=10,blank=True)
    CreateTime   = models.DateTimeField(auto_now=True)
    def __str__(self):
       return str(self.id)


#------cart-------------------
class Req_info(models.Model):
    RestuarantID=models.ForeignKey(Restuarant, on_delete=models.CASCADE)
    CustomerID=models.ForeignKey(User, on_delete=models.CASCADE)
    status=models.CharField(max_length=255, default='Pending')
    GrandTotal=models.FloatField(  null=True,default='0.00' )
    Address = models.CharField(max_length=255,null=True)
    Phone = models.CharField(max_length=15,null=True)
    EntryDate = models.DateTimeField(auto_now=True)
    def __str__(self):
      return str(self.id)

class OrderDetails(models.Model):
    orderID = models.ForeignKey(Req_info, on_delete=models.CASCADE)
    FoodID=models.ForeignKey(Product, on_delete=models.CASCADE,)
    Foodname = models.CharField(max_length=150)
    FoodSize = models.CharField(max_length=100)
    Foodprice = models.FloatField()
    Foodquantity= models.FloatField()
    EntryDate = models.DateTimeField(auto_now=True)
    def __str__(self):
      return str(self.orderID)
#--------endcart---------------

class Ratings(models.Model):
  ProductID=models.ForeignKey(Product, on_delete=models.CASCADE)
  UserID=models.ForeignKey(User, on_delete=models.CASCADE)
  orderID = models.ForeignKey(Req_info, on_delete=models.CASCADE)
  Rate=models.IntegerField()
  EntryDate = models.DateTimeField(auto_now=True)
  def __str__(self):
    return str(self.id)

class RembemberRating(models.Model):
  ProductID=models.ForeignKey(Product, on_delete=models.CASCADE)
  orderID = models.ForeignKey(Req_info, on_delete=models.CASCADE)
  Rate=models.IntegerField(default=0)
  EntryDate = models.DateTimeField(auto_now=True)
  def __str__(self):
    return str(self.id)