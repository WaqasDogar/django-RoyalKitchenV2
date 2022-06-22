# templatetags/tag_library.py
from django import template
from django.db.models.fields import EmailField
register = template.Library()

from Myapp.models import *

@register.filter()
def to_int(value):
    return value.id

@register.filter()
def get_mail(value):
    obj=User.objects.all()
    for val in obj:
        if str(val)==str(value):
         return str(val.email)
         
@register.filter()
def to_str(value):
    return str(value)

#--------my tags for new royal kitchen

@register.filter()
def id_to_restuarantname(value):
    try:
        val=User.objects.get(username=value)
        #val=Restuarant.objects.get(id=value)
        return str(val.first_name)
    except:
        val=Restuarant.objects.get(id=value.id)
        #ak srf set kr k dusre trf deckhda
        return  "nichla"# str(val.RestuarantName)

@register.filter()
def id_to_restuarantnamebycart(value):
        val=Restuarant.objects.get(id=value)
        return val.RestuarantName

@register.filter()  
def id_to_restuarantnamebyordrs(value):
    val=Restuarant.objects.get(id=value.id)
    return val.RestuarantName
    
@register.filter()
def id_to_username(value):
    usr=User.objects.get(id=value.id)
    return str(usr).capitalize()

@register.filter()
def Approvel_Check(resid):
    uobj=User.objects.get(username=resid)
    obj=Restuarant.objects.get(RestuarantID=uobj)
    if str(obj.Status).upper()=="PENDING" or str(obj.Status).upper()=="REJECTED":
        return False
    else:
        return True

@register.filter()
def Billcheck(resid):
    uobj=User.objects.get(username=resid)
    obj=Restuarant.objects.get(RestuarantID=uobj)
    bill=Billing.objects.get(RestuarantID=resid)
    if str(bill.Status).upper()!="PAID":
        return False
    else:
        return True

@register.filter()  
def get_rest_image(value):
    val=Restuarant.objects.get(id=value.id)
    rexource=WebResources.objects.get(RestuarantID=val)
    return rexource.Image.url
    
@register.filter()  
def get1stproduct(value):
    val=Restuarant.objects.get(id=value.id)
    prod=Product.objects.filter(RestuarantID=val)
    for data in prod:
        return data.Foodimage.url
    
@register.filter()  
def get1stproductprice(value):
    val=Restuarant.objects.get(id=value.id)
    prod=Product.objects.filter(RestuarantID=val)
    for data in prod:
        return data.Foodprice

@register.filter()  
def productcount(value):
    val=Restuarant.objects.get(id=value.id)
    if Product.objects.filter(RestuarantID=val).count()>0:
        return True
    else:
        return False
    
@register.filter()
def ratingstatuscheck(oid,pid):
    print(oid,pid)
    if RembemberRating.objects.filter(orderID=oid,ProductID=pid).count()>0:
        return False
    else:
        return True

@register.filter(name='times') 
def times(number):
    return range(number)

@register.filter()
def getorderproductsrating(oid,pid):
    obj=RembemberRating.objects.get(orderID=oid,ProductID=pid)
    return obj.Rate
    
@register.filter()
def getproductrating(pid):
    ratings=Ratings.objects.filter(ProductID=pid)
    sum=0
    count=0
    for data in ratings:
        sum+=data.Rate
        count+=1
    if count==0:
        return 0
    else:
        return sum/count

@register.filter()
def getproductstars(pid):
    ratings=Ratings.objects.filter(ProductID=pid)
    sum=0
    for data in ratings:
        sum+=data.Rate
    return sum

@register.filter()
def getproduct_restuarant_name(pid):
    prodobj=Product.objects.get(id=pid.id)
    return prodobj.RestuarantID.RestuarantName

@register.filter()
def get_prod_res_city(pid):
    prodobj=Product.objects.get(id=pid.id)
    return prodobj.RestuarantID.RestuarantCity

@register.filter()
def getproduct_name(pid):
    prodobj=Product.objects.get(id=pid.id)
    return prodobj.Foodsize+" "+prodobj.Foodname

@register.filter()
def getproduct_price(pid):
    prodobj=Product.objects.get(id=pid.id)
    return prodobj.Foodprice

@register.filter()
def getproduct_restuarantid(pid):
    prodobj=Product.objects.get(id=pid.id)
    return prodobj.RestuarantID.id

@register.filter()
def getproduct_restuarantobject(pid):
    prodobj=Product.objects.get(id=pid.id)
    return prodobj.RestuarantID

@register.filter()
def getproduct_image(pid):
    prodobj=Product.objects.get(id=pid.id)
    return prodobj.Foodimage.url
    

@register.filter()
def getresturantrating(resid):
    obj=Restuarant.objects.get(id=resid.id)
    pro=Product.objects.filter(RestuarantID=obj)
    ressum=0
    for ids in pro:
        ratings=Ratings.objects.filter(ProductID=ids.id)
        sum=0
        count=0
        for data in ratings:
            sum+=data.Rate
            count+=1
        if count==0:
            pass
        else:
            ressum+= sum/count
    return ressum