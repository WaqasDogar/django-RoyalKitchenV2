from django.contrib import admin
from .models import *
# Register your models here.

class classOffers(admin.ModelAdmin):
    list_display=['id','RestuarantID','OfferName','OfferPrice','OfferDescription','Availability','CreateTime']
class classEmployee(admin.ModelAdmin):
    list_display=['id','RestuarantID','FirstName','LastName','CNIC','FatherName','Age','Gender','EntryDate']
class ClassDelivery(admin.ModelAdmin):
    list_display=['id','RestuarantID','EmployeePID','CustomerOrderID','DeliveryAddress','ExpectedTime','EntryDate']
class ClassFeeds(admin.ModelAdmin):
    list_display=['id','RestuarantID','Username','Email','Comment','EntryDate']
class ClassWebResources(admin.ModelAdmin):
    list_display=['id','RestuarantID','Image','IDfront','IDblack','Location','Phone1','Phone2','Day','OpeningTime','ClosingTime','LinkedInLink','GitLink','TwitterLink','FbLink','EntryDate']
class ClassManager(admin.ModelAdmin):
    list_display=['id','RestuarantID','Image','Name','Rank','EntryDate']
class classproduct(admin.ModelAdmin):
    list_display=['id','RestuarantID','Foodname','Foodsize','Foodprice','Fooddescription','Foodimage','EntryDate']
class classRestuarant(admin.ModelAdmin):
    list_display=['id','RestuarantID','RestuarantName','RestuarantCity','RestuarantState','RestuarantCountry','Status']
class classBilling(admin.ModelAdmin):
    list_display=['id','RestuarantID','Status','Amount','DateFrom','DateTo','EntryDate']
class classUserType(admin.ModelAdmin):
    list_display=['id','UserID','UserType','EntryDate']

class classBankAccount(admin.ModelAdmin):
    list_display=['BillingID','TransactionID','BankName','AccountNumber','CustomerName','EntryDate']
class classCompletedPayments(admin.ModelAdmin):
    list_display=['id','RestuarantID','Status','Amount','DateFrom','DateTo','EntryDate']

class classUserProfile(admin.ModelAdmin):
    list_display=['id','UserID','Image','EntryDate']

class classRatings(admin.ModelAdmin):
    list_display=['id','ProductID','UserID','orderID','Rate','EntryDate']

class classRembemberRating(admin.ModelAdmin):
    list_display=['id','ProductID','orderID','Rate','EntryDate']

admin.site.register(Restuarant,classRestuarant)
admin.site.register(Offers,classOffers)
admin.site.register(Billing,classBilling)
admin.site.register(Employee,classEmployee)
admin.site.register(Delivery,ClassDelivery)
admin.site.register(Feeds,ClassFeeds)
admin.site.register(WebResources,ClassWebResources)
admin.site.register(Manager,ClassManager)
admin.site.register(Product,classproduct)
admin.site.register(UserType,classUserType)
admin.site.register(BankAccount,classBankAccount)
admin.site.register(CompletedPayments,classCompletedPayments)
admin.site.register(Ratings,classRatings)
admin.site.register(RembemberRating,classRembemberRating)


#----cart----
admin.site.register(OrderDetails)
#-------combine list
class OrderItemInline(admin.TabularInline):
    model = OrderDetails
    raw_id_fields = ['orderID']

@admin.register(Req_info)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id']
    #list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
#------endcart-----