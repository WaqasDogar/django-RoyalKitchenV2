from datetime import date, datetime
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from .models import *
import reverse_geocoder as rg
from .cart import Cart
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.models import User
from .forms import *
from django.contrib import messages 
import smtplib, ssl
from email.mime.text import MIMEText

#import pprint
#reason for order rejection in orders history
#ratingwise restuarant on top of list
#forign key data method:  data.RestuarantID.datafrom primarykey table
# Create your views here.

def maintemp(request):
    return render(request,"Myapp/newindex.html")

def reverseGeocode(coordinates):
    result=rg.search(coordinates)
    print(result[0]['name'])
    print(result[0]['admin1'])
    print(result[0]['cc'])
    print("\n\n")
    return result
    #pprint.pprint(result)

def Vendor(request):
    usr=User.objects.get(username=request.user)
    if UserProfile.objects.filter(UserID=request.user).count()>0:
        profile=UserProfile.objects.get(UserID=request.user)
        
        res=Restuarant.objects.get(RestuarantID=usr)
        order=Req_info.objects.filter(RestuarantID=res)
        products=OrderDetails.objects.all()
        if request.method=="POST":
            if request.POST.get("search") is not None:
                order=Req_info.objects.filter(RestuarantID=res,id__contains=request.POST.get("search"))

        tpending=Req_info.objects.filter(RestuarantID=res,status="Pending").count()
        tapproved=Req_info.objects.filter(RestuarantID=res,status="Approved").count()
        trejected=Req_info.objects.filter(RestuarantID=res,status="Rejected").count()
        tdelivered=Req_info.objects.filter(RestuarantID=res,status="Received").count()

        sum=0
        objtotal=Req_info.objects.filter(RestuarantID=res,status="Approved")
        for d in objtotal:
            sum+=d.GrandTotal

        data={
        "order":order,
        "products":products,
        "res":res,
        "totalsale":sum,
        "tpen":tpending,
        "tapp":tapproved,
        "trej":trejected,
        "tdel":tdelivered,
        "profile":profile
        }
        return render(request,"Myapp/Vendor.html",data)
    
    res=Restuarant.objects.get(RestuarantID=usr)
    order=Req_info.objects.filter(RestuarantID=res)

    if request.method=="POST":
        if request.POST.get("search") is not None:
            order=Req_info.objects.filter(RestuarantID=res,id__contains=request.POST.get("search"))

    
    products=OrderDetails.objects.all()
    tpending=Req_info.objects.filter(RestuarantID=res,status="Pending").count()
    tapproved=Req_info.objects.filter(RestuarantID=res,status="Approved").count()
    trejected=Req_info.objects.filter(RestuarantID=res,status="Rejected").count()
    tdelivered=Req_info.objects.filter(RestuarantID=res,status="Received").count()

    sum=0
    objtotal=Req_info.objects.filter(RestuarantID=res,status="Approved")
    for d in objtotal:
        sum+=d.GrandTotal
    data={
        "order":order,
        "products":products,
        "res":res,
        "totalsale":sum,
        "tpen":tpending,
        "tapp":tapproved,
        "trej":trejected,
        "tdel":tdelivered,
        }
    
    return render(request,"Myapp/Vendor.html",data)

def orderstatus(request,oid):
    Req_info.objects.filter(id=oid).update(status="Received")
    return redirect("userorder")

def Approve(request,dataid,cusid):
    id=dataid
    name=cusid

    usr=User.objects.get(username=request.user)
    res=Restuarant.objects.get(RestuarantID=usr)
    #getting foods from the order
    odrfood=""
    foods=OrderDetails.objects.all()
    for val in foods:
        if(str(val.orderID)==str(id)):
            odrfood=odrfood+"[Food Name: "+val.Foodname+" | Size:"+str(val.FoodSize)+" | Qty:"+str(int(val.Foodquantity))+" | Price: "+str(val.Foodprice)+"]\n"
    
    objid=Req_info.objects.get(id=id)
    odrfood=odrfood+"\n[Grand Total: "+str(objid.GrandTotal)+"]"

    #getting user email address
    usr="empty"
    objj=User.objects.all()
    for val in objj:
        if str(val)==name:
            usr=val.email
    useremail=usr

    #getting phone number from database------------------------------------------
    objid=Req_info.objects.get(id=id)
    test_str=str(objid.Phone)
    new_str = ''.join([test_str[i] for i in range(len(test_str)) if i != 0])
    phonenumber="+92"+new_str
    # till now-------------------------------------------------------------------
    #sending messege to phone number ----------------------------------------------------------

    from twilio.rest import Client
    try:
       
        client = Client(account_sid, auth_token) 
        
        message = client.messages.create( 
                                    from_='whatsapp:+14155238886',  
                                    body='Order#'+str(id)+' Approved <- Royal Kitchen''S.'+'Dear '+ name +' your Order is Approved and will be delivered soon in less than 45 minutes. Order Details'+odrfood+' Thanks for choosing '+res.RestuarantName+'--Royal KitchenS Community.',
                                    to='whatsapp:'+phonenumber
                                ) 
    except Exception as e:
        print(e)
    

     #by using useremail sending email to the user 
    #by using useremail sending email to the user 
   # try:
    sender = 'mozaua15@gmail.com'
    receivers = [useremail]
    body_of_email = 'Dear '+ name +' your Order is Approved and will be delivered soon in less than 45 minutes. Order Details'+odrfood+' Thanks for choosing '+res.RestuarantName+'--Royal KitchenS Community.'
    msg = MIMEText(body_of_email, 'html')
    msg['Subject'] = 'Order#'+str(id)+' Approved <- Royal Kitchen''S'
    msg['From'] = sender
    msg['To'] = ','.join(receivers)
    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = 'mozaua15@gmail.com', password = 'wikzxztiyqfiigag')
    s.sendmail(sender, receivers, msg.as_string())
    s.quit()
    print("Email has been sent sucessfully!")
    #except:
    #    messages.add_message(request,messages.INFO,'ERROR! Email Not sent')
        

    Req_info.objects.filter(id=dataid).update(status="Approved")
    return template(request)

def Reject(request,dataid,cusid):
    id=dataid
    name=cusid
    #getting user email address
    usr="empty"
    objj=User.objects.all()
    for val in objj:
        if str(val)==name:
            usr=val.email
    useremail=usr
    #getting phone number from database------------------------------------------
    objid=Req_info.objects.get(id=id)
    test_str=str(objid.Phone)
    new_str = ''.join([test_str[i] for i in range(len(test_str)) if i != 0])
    phonenumber="+92"+new_str
    # till now-------------------------------------------------------------------
    #sending messege to phone number ----------------------------------------------------------

    usr=User.objects.get(username=request.user)
    res=Restuarant.objects.get(RestuarantID=usr)

    from twilio.rest import Client
    try:
        
        client = Client(account_sid, auth_token) 
        
        message = client.messages.create( 
                                    from_='whatsapp:+14155238886',  
                                    body='Order#'+str(id)+' Rejected <-- '+res.RestuarantName+'. Dear '+ name +' we are really sorry :( Your Order is Rejected for further details contact '+res.RestuarantName,
                                    to='whatsapp:'+phonenumber
                                ) 
    except Exception as e:
        print(e)


    try:
        sender = 'mozaua15@gmail.com'
        receivers = [useremail]
        body_of_email = 'Dear '+ name +' we are really sorry :( Your Order is Rejected for further details contact '+res.RestuarantName
        msg = MIMEText(body_of_email, 'html')
        msg['Subject'] = 'Order Rejected -> Royal Kitchen''S'
        msg['From'] = sender
        msg['To'] = ','.join(receivers)
        s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
        s.login(user = 'mozaua15@gmail.com', password = 'wikzxztiyqfiigag')
        s.sendmail(sender, receivers, msg.as_string())
        s.quit()
        print("Email has been sent sucessfully!")
    except:
        messages.add_message(request,messages.INFO,'ERROR! Email Not sent')
    Req_info.objects.filter(id=dataid).update(status="Rejected")
    return template(request)

def get_rated_products_desendingorder():
    dt={}
    rate=Ratings.objects.all()
    for data in rate:
        data.ProductID
        if data.ProductID in dt.keys():
            dt[data.ProductID]+=data.Rate
        else:
            dt[data.ProductID]=data.Rate
               
    import operator
    sorted_d={}
    for data in dt:
        print(dt[data]) 
        print(data)
        sorted_d = dict( sorted(dt.items(), key=operator.itemgetter(1),reverse=True))
    l=[]
    for data in sorted_d:
        l.append(data)
    return l

import random

def foo(request):
    num=request.session.get('num')
    if num is None:
        num=random.randint(100000,999999)
    request.session['num']=num

def forget(request):
    try:
        if request.method =="POST":
            username=request.POST['username']
            obj=User.objects.get(username=username)
            useremail=obj.email
            foo(request)
            ##############sending email###########################
            try:
                sender = 'mozaua15@gmail.com'
                receivers = [useremail]
                body_of_email = 'Your OTP pin code is: '+str(request.session.get('num'))
                msg = MIMEText(body_of_email, 'html')
                msg['Subject'] = username+' wanna forget password?'
                msg['From'] = sender
                msg['To'] = ','.join(receivers)
                s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
                s.login(user = 'mozaua15@gmail.com', password = 'wikzxztiyqfiigag')
                s.sendmail(sender, receivers, msg.as_string())
                s.quit()
                print("Email has been sent sucessfully!")
            except:
                messages.add_message(request,messages.INFO,'ERROR! Email Not sent')
                return redirect('forget')
            return render(request,'Myapp/forgetconfirm.html',{'username':username})
                ######################################################
    except:
        messages.add_message(request,messages.INFO,'ERROR! User Does not exists')
    return render(request,'Myapp/forget.html')

def forgetconfirm(request):
    if request.method=="POST":
        usr=request.POST['usernm']
        otp=request.POST['OTP']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        obj=User.objects.get(username=usr)
        if str(otp)==str(request.session.get('num')):
            if pass1==pass2:
                    if pass1.__len__()>=5:
                        obj.set_password(pass1)
                        obj.save()
                        return redirect('signin')
                    else:
                        messages.add_message(request,messages.INFO,'Password Is too Short. Must be 5 characters long')
            else:
                messages.add_message(request,messages.INFO,'Password Mismatched')
        else:
            messages.add_message(request,messages.INFO,'Wrong OTP')

    return render(request,'Myapp/forgetconfirm.html')

def template(request):
    if request.method=="POST":
        if request.POST.get("search") is not None:
            return redirect("Searchindex",request.POST.get("search"))

    ratedpros=get_rated_products_desendingorder()
    usr=request.user
    typename=""
    if str(usr) !="AnonymousUser":
        if request.user.is_superuser:
            return redirect('http://127.0.0.1:8000/admin/')
        usrtyp=UserType.objects.get(UserID=usr)
        typename=usrtyp.UserType
        print(usrtyp.UserType)
    
    if typename=="CUSTOMER":
        qs=WebResources.objects.all()
        Data=qs.only('RestuarantID').distinct()
        print(Data)
        #resource= WebResources.objects.select_related('RestuarantID')
        print("======================================================================")
        try:
            if request.method=="POST":
                if request.POST.get("longi") is not None:
                    # Get the post parameters
                    longi=request.POST['longi']
                    lanti=request.POST['lanti']
                    coordinates =(float(lanti),float(longi))
                    result=reverseGeocode(coordinates)
                    city=result[0]['name']
                    state=result[0]['admin1']
                    country=result[0]['cc']
                    NewData=[]
                    for x in Data:
                        if(x.RestuarantID.RestuarantCity==city):
                            NewData.append(x)
                    if UserProfile.objects.filter(UserID=request.user).count()>0:
                        profile=UserProfile.objects.get(UserID=request.user)
                        user=User.objects.get(username=request.user)
                        return render(request,'Myapp/index.html',{'resturant':NewData,'loc':city+","+state+","+country,"profile":profile,"ratedpros":ratedpros})

                    return render(request,'Myapp/index.html',{'resturant':NewData,'loc':city+","+state+","+country,"ratedpros":ratedpros})
        except:
            return render(request,'Myapp/index.html',{'restuarant':Data,'loc':"Location service not available","ratedpros":ratedpros})

        if UserProfile.objects.filter(UserID=request.user).count()>0:
                profile=UserProfile.objects.get(UserID=request.user)
                user=User.objects.get(username=request.user)
                return render(request,'Myapp/index.html',{'resturant':Data,"profile":profile,"ratedpros":ratedpros})

        return render(request,'Myapp/index.html',{'resturant':Data,"ratedpros":ratedpros})

    elif typename=="VENDOR":
        user=request.user
        #####################################################################################
        robject=Restuarant.objects.filter(RestuarantID=user)
        if robject.count()>0:
            robj=Restuarant.objects.get(RestuarantID=user)
            ###########################333
            billobj=Billing.objects.filter(RestuarantID=robj)
            if billobj.count()>0:
                billobjnew=Billing.objects.get(RestuarantID=robj)
                if str(billobjnew.Status).upper()=="PENDING":
                    return  redirect("VendorTransaction") # render(request,'Myapp/signinVendor.html',{'pas':"Please pay your dues:"+str(billobjnew.Amount)+" to continue."})
                elif str(billobjnew.Status).upper()=="REQUESTED":
                    logout(request)
                    return  render(request,'Myapp/signinVendor.html',{'pas':"We are sorry your transaction is not yet verified!"})
                else:
                    if str(robj.Status).upper()=="PENDING":
                        return  render(request,'Myapp/signinVendor.html',{'pas':"Sorry! Your account is under review or not approved yet."})
                    elif str(robj.Status).upper()=="REJECTED":
                        return  render(request,'Myapp/signinVendor.html',{'pas':"Your account is rejected email us for more details."})
                    else:
                        if bill_expired(billobjnew.DateTo):
                            print("Yes its expired")
                            CompletedPayments.objects.create(RestuarantID=billobjnew.RestuarantID,Status="Cleared",Amount=billobjnew.Amount,DateFrom=billobjnew.DateFrom,DateTo=billobjnew.DateTo)
                            billobjnew.delete()
                            login(request,user)
                            return redirect("Vendorpayments")

                        login(request,user)
                        return redirect('Vendor')

            elif billobj.count()==0:
                return redirect("Vendorpayments")
            ###########################333    
        else:
            login(request,user)
            return redirect("ResRegistration")
                    #####################################################################################

    else:
        qs=WebResources.objects.all()
        Data=qs.only('RestuarantID').distinct()
        #resource= WebResources.objects.select_related('RestuarantID')
        print("======================================================================")
        try:
            if request.method=="POST":
                # Get the post parameters
                longi=request.POST['longi']
                lanti=request.POST['lanti']
                coordinates =(float(lanti),float(longi))
                result=reverseGeocode(coordinates)
                city=result[0]['name']
                state=result[0]['admin1']
                country=result[0]['cc']
                NewData=[]
                for x in Data:
                    if(x.RestuarantID.RestuarantCity==city):
                        NewData.append(x)
                return render(request,'Myapp/index.html',{'resturant':NewData,'loc':city+","+state+","+country,"ratedpros":ratedpros})
        except:
            return render(request,'Myapp/index.html',{'restuarant':Data,'loc':"Location service not available"})
        return render(request,'Myapp/index.html',{'resturant':Data,"loc":"Click on detect button..","ratedpros":ratedpros})
    
def Searchindex(request,searchquerry):
    if request.method=="POST":
        if request.POST.get("search") is not None:
            searchquerry=request.POST.get("search")

    srchrests=Restuarant.objects.filter(RestuarantName__contains=searchquerry)
    srchpros=Product.objects.filter(Foodname__contains=searchquerry)

    restscount=srchrests.count()
    proscount=srchpros.count()
    if str(request.user) !="AnonymousUser":
        if UserProfile.objects.filter(UserID=request.user).count()>0:
                profile=UserProfile.objects.get(UserID=request.user)
                return render(request,"Myapp/Searchindex.html",{"rests":srchrests,"pros":srchpros,"profile":profile,"restcount":restscount,"proscount":proscount})
    return render(request,"Myapp/Searchindex.html",{"rests":srchrests,"pros":srchpros,"restcount":restscount,"proscount":proscount})


def userorder(request):
    ordrobj=Req_info.objects.filter(CustomerID=request.user)
    ordrprod=OrderDetails.objects.all()
    msg=""
    if ordrobj.count()==0:
        msg="No order's available"
    
    if request.method=="POST":
        if request.POST.get("rate") is not None:
            rate=request.POST.get("rate")
            pid=request.POST.get("pid")
            pid=Product.objects.get(id=pid)
            oid=request.POST.get("oid")
            odrid=Req_info.objects.get(id=oid)
            if Ratings.objects.filter(ProductID=pid,UserID=request.user).count()>0:
                Ratings.objects.filter(ProductID=pid,UserID=request.user).update(Rate=rate)
                RembemberRating.objects.create(ProductID=pid,orderID=odrid,Rate=rate)
            else:
                Ratings.objects.create(ProductID=pid,UserID=request.user,orderID=odrid,Rate=rate)
                RembemberRating.objects.create(ProductID=pid,orderID=odrid,Rate=rate)

    if UserProfile.objects.filter(UserID=request.user).count()>0:
                profile=UserProfile.objects.get(UserID=request.user)
                user=User.objects.get(username=request.user)
                return render(request, 'Myapp/Orders.html',{"Order":ordrobj,"OrderProducts":ordrprod,"msg":msg,"profile":profile}) 

    return render(request, 'Myapp/Orders.html',{"Order":ordrobj,"OrderProducts":ordrprod,"msg":msg})       

def useraccount(request):
    form1= User.objects.get(username=request.user)
    form=userform(instance=form1)
    if request.method == 'POST':
        if request.FILES.get('tasveer') is not None:
            if UserProfile.objects.filter(UserID=request.user).count()>0:
                UserProfile.objects.filter(UserID=request.user).delete()
                UserProfile.objects.create(UserID=request.user,Image=request.FILES['tasveer'])
            else:
                UserProfile.objects.create(UserID=request.user,Image=request.FILES['tasveer'])

        if request.POST.get("username") is not None:
            form = userform(request.POST,instance=form1)
            if form.is_valid:
                form.save()
            else:
                messages.add_message(request,messages.INFO,'Input Data is not Valid')

    if UserProfile.objects.filter(UserID=request.user).count()>0:
        profile=UserProfile.objects.get(UserID=request.user)
        user=User.objects.get(username=request.user)
        return render(request, 'Myapp/Userprofile.html',{'form':user,"profile":profile})    

    user=User.objects.get(username=request.user)
    return render(request, 'Myapp/Userprofile.html',{'form':user})    

def Signup(request):
    if request.method=="POST":
        try:
            # Get the post parameters
            username=request.POST['Username']
            email=request.POST['email']
            pass1=request.POST['password1']
            pass2=request.POST['password2']

            # check for passwords if matching ot not 
            if (pass1!= pass2):
                return render(request, 'Myapp/signup.html',{"pas":"Passwords do not match"})
            # Create the user
            myuser = User.objects.create_user(username, email, pass1)
            myuser.save()
            UserType.objects.create(UserID=myuser,UserType="CUSTOMER")
            return redirect('signin')
        except Exception as e:
            return render(request, 'Myapp/signup.html',{"pas":e})

    return render(request, 'Myapp/signup.html')

def Login(request):
    try:
        if request.method=="POST":
            # Get the post parameters
            loginusername=request.POST['Username']
            loginpassword=request.POST['password']

            user=authenticate(username= loginusername, password= loginpassword)
            if user is not None:
                utid=UserType.objects.get(UserID=user)
                if utid.UserType=="CUSTOMER":
                    login(request,user)
                    return redirect("index")
                else:
                    return  render(request,'Myapp/signin.html',{'pas':"Login Unsuccessfull"})
            else:
                return  render(request,'Myapp/signin.html',{'pas':"User Doesn't exist || Wrong Credentials"})
        return render(request,'Myapp/signin.html')
    except Exception as e:
        return  render(request,'Myapp/signin.html',{'pas':e})

def bill_expired(var):
    date1=str(var)
    newdate1=""
    for x in date1:
        if x=='+':
            break
        newdate1+=x
    newdate1=newdate1.replace('-','/')
    from datetime import datetime
    date_time_str = newdate1
    date_time_obj = datetime.strptime(date_time_str, '%Y/%m/%d %H:%M:%S')
    past=date_time_obj.date()
    present = datetime.now()
    return past < present.date()

def signinVendor(request):
    try:
        if request.method=="POST":
            # Get the post parameters
            loginusername=request.POST['Username']
            loginpassword=request.POST['password']

            user=authenticate(username= loginusername, password= loginpassword)
            if user is not None:
                utid=UserType.objects.get(UserID=user)
                if utid.UserType=="VENDOR":
                    #####################################################################################
                    robject=Restuarant.objects.filter(RestuarantID=user)
                    if robject.count()>0:
                        robj=Restuarant.objects.get(RestuarantID=user)
                        ###########################333
                        billobj=Billing.objects.filter(RestuarantID=robj)
                        if billobj.count()>0:
                            billobjnew=Billing.objects.get(RestuarantID=robj)
                            ##if billing is expired to usy payments pr ly jao
                            if str(billobjnew.Status).upper()=="PENDING":
                                login(request,user)
                                return redirect("VendorTransaction") # render(request,'Myapp/signinVendor.html',{'pas':"Please pay your dues:"+str(billobjnew.Amount)+" to continue."})
                            elif str(billobjnew.Status).upper()=="REQUESTED":
                                login(request,user)
                                return  render(request,'Myapp/signinVendor.html',{'pas':"We are sorry your transaction is not yet verified!"})
                                    
                            else:
                                if str(robj.Status).upper()=="PENDING":
                                    return  render(request,'Myapp/signinVendor.html',{'pas':"Sorry! Your account is under review or not approved yet."})
                                elif str(robj.Status).upper()=="REJECTED":
                                    return  render(request,'Myapp/signinVendor.html',{'pas':"Your account is rejected email us for more details."})
                                else:
                                    if bill_expired(billobjnew.DateTo):
                                        print("Yes its expired")
                                        CompletedPayments.objects.create(RestuarantID=billobjnew.RestuarantID,Status="Cleared",Amount=billobjnew.Amount,DateFrom=billobjnew.DateFrom,DateTo=billobjnew.DateTo)
                                        billobjnew.delete()
                                        login(request,user)
                                        return redirect("Vendorpayments")
                                    ############################
                                    login(request,user)
                                    return redirect('Vendor')

                        elif billobj.count()==0:
                            login(request,user)
                            return redirect("Vendorpayments")
                    else:
                        login(request,user)
                        return redirect("ResRegistration")
                    #####################################################################################
                else:
                    return  render(request,'Myapp/signinVendor.html',{'pas':"Login Unsuccessfull"})
            else:
                return  render(request,'Myapp/signinVendor.html',{'pas':"User Doesn't exist || Wrong Credentials"})
        return render(request,'Myapp/signinVendor.html')
    except Exception as e:
        return  render(request,'Myapp/signinVendor.html',{'pas':e})

def ResRegistration(request):
    try:
        if request.method=="POST":
            if request.POST.get("longi") is not None:
                # Get the post parameters
                longi=request.POST['longi']
                lanti=request.POST['lanti']
                coordinates =(float(lanti),float(longi))
                result=reverseGeocode(coordinates)
                city=result[0]['name']
                state=result[0]['admin1']
                country=result[0]['cc']
                return render(request,"Myapp/ResRegistration.html",{"city":city,"state":state,"country":country})
            
            if request.POST.get("resname") is not None:
                uobj=User.objects.get(username=request.user)
                newrestuarant=Restuarant.objects.create(
                    RestuarantID=uobj,
                    RestuarantName=request.POST.get("resname"),
                    RestuarantCity=request.POST.get("city"),
                    RestuarantState=request.POST.get("state"),
                    RestuarantCountry=request.POST.get("country"),
                    Status="PENDING")
                
                WebResources.objects.create(
                    RestuarantID=newrestuarant,
                    Image=request.FILES['resimage'],
                    IDfront=request.FILES['cnicfront'],
                    IDblack=request.FILES['cnicback'],
                    Location=request.POST.get("location"),
                    Phone1=request.POST.get("phone1"),
                    Phone2=request.POST.get("phone2"))

                return redirect('Vendorpayments')

        return render(request,"Myapp/ResRegistration.html")
    except Exception as e:
        return HttpResponseBadRequest(e)

def Vendorpayments(request):
    user=request.user
    usrobj=User.objects.get(username=user)
    resobj=Restuarant.objects.get(RestuarantID=usrobj)

    if request.method=="POST":
        if request.POST.get("resid") is not None:
            request.POST.get("resid")
            dfrom=str(request.POST.get("dfrom"))
            dto=str(request.POST.get("dto"))
            import datetime 
            datem1 = datetime.datetime.strptime(dfrom, "%Y-%m-%d")
            datem2 = datetime.datetime.strptime(dto, "%Y-%m-%d")
            
            from datetime import date as date_n  
            date_1 = date_n(datem1.year,datem1.month,datem1.day)  
            date_2 = date_n(datem2.year,datem2.month,datem2.day)  
            dins=(date_2 - date_1).days  
            totalbill=int(dins)*500

            resobj=Restuarant.objects.get(RestuarantID=request.user)
            if Billing.objects.filter(RestuarantID=resobj).count()>0:
                Billing.objects.filter(RestuarantID=resobj).update(Status="Pending",Amount=totalbill,DateFrom=date_1,DateTo=date_2)
            else:
                Billing.objects.create(RestuarantID=resobj,Status="Pending",Amount=totalbill,DateFrom=date_1,DateTo=date_2)
            
            return redirect("VendorTransaction")
            return HttpResponseBadRequest("Your total Bill is: "+str(totalbill)+" Pay it on Our account number| 03131272822 |Jazzcash Account |Muhammad Waqas Khalid")
            return render(request,"Myapp/VendorPayments.html",{"res":resobj,"totalbill":totalbill})

    
    return render(request,"Myapp/Vendorpayments.html",{"res":resobj})

def VendorTransaction(request):
    resobj=Restuarant.objects.get(RestuarantID=request.user)
    Bobj=Billing.objects.get(RestuarantID=resobj)
    if request.method=="POST":
        if request.POST.get("resid") is not None:
            BankAccount.objects.create(BillingID=Bobj,TransactionID=request.POST.get("tid"),BankName=request.POST.get("bname"),AccountNumber=request.POST.get("bnum"),CustomerName=request.POST.get("holder"))
            Billing.objects.filter(RestuarantID=resobj).update(Status="REQUESTED")
            return redirect("signinVendor")
    
    return render(request,"Myapp/VendorTransaction.html",{"bill":Bobj})

def vendorbilling(request):
    resobj=Restuarant.objects.get(RestuarantID=request.user)
    Bobj=Billing.objects.get(RestuarantID=resobj)
    return render(request,"Myapp/VendorBills.html",{"bill":Bobj})

def signupVendor(request):
    if request.method=="POST":
        try:
            # Get the post parameters
            username=request.POST['Username']
            email=request.POST['email']
            pass1=request.POST['password1']
            pass2=request.POST['password2']

            # check for passwords if matching ot not 
            if (pass1!= pass2):
                return render(request, 'Myapp/signupVendor.html',{"pas":"Passwords do not match"})
            # Create the user
            myuser = User.objects.create_user(username, email, pass1)
            myuser.save()
            UserType.objects.create(UserID=myuser,UserType="VENDOR")
            return redirect('signinVendor')
        except Exception as e:
            return render(request, 'Myapp/signupVendor.html',{"pas":e})

    return render(request, 'Myapp/signupVendor.html')

def Foods(request,RestID):
    obj=Restuarant.objects.get(id=RestID)
    if request.method=="POST":
        if request.POST.get("foodname") is not None:
            Product.objects.create(
                RestuarantID=obj,
                Foodname=request.POST.get("foodname"),
                Foodprice=request.POST.get("price"),
                Foodsize=request.POST.get("size"),
                Fooddescription=request.POST.get("desc"),
                Foodimage=request.FILES['photo'])

    foods=Product.objects.filter(RestuarantID=RestID)    

    return render(request,"Myapp/RestuarantFoods.html",{"product":foods})

def updatepro(request,PID):
    form= Product.objects.get(id=PID)
    if request.method == 'POST':
        if request.POST.get("name") is not None:
           obj= Product.objects.filter(id=PID).update(
                Foodname=request.POST.get("name"),
                Foodprice=request.POST.get("price"),
                Foodsize=request.POST.get("size"),
                Fooddescription=request.POST.get("desc"))
           

    form= Product.objects.get(id=PID)
    return render(request,'Myapp/updatepro.html',{"form":form})

# def updatepro(request,PID):
#     form1= Product.objects.get(id=PID)
#     form=proform(instance=form1)
#     if request.method == 'POST':
#         form = proform(request.POST,request.FILES,instance=form1)
#         if form.is_valid:
#             form.save()
#             return redirect('Vendor')
#     context ={'form':form1}
#     return render(request,'Myapp/updatepro.html',context)

def deletepro(request,PID):
    obj=Product.objects.get(id=PID)
    obj.delete()
    return redirect('Vendor')

def Logout(request):
    logout(request)
    return redirect('index')

def restuarant(request,id):
    obj=Restuarant.objects.get(id=id)
    foods=Product.objects.filter(RestuarantID=id)
    offers=Offers.objects.filter(RestuarantID=id)

    count=1
    if(offers.count()==0):
        count=0
    
    resid=obj.id
    resowner=obj.RestuarantID
    resname=obj.RestuarantName  
    
    resource=WebResources.objects.filter(RestuarantID=id)
    test=WebResources.objects.get(RestuarantID=id)
    photo=test.Image
    
    context={
        'photo':photo,
        'resource':resource,
        'resname':resname,
        'resowner':resowner,
        'product':foods,
        'offers':offers,
        'count':count,
        'resid':resid
        }
    return render(request,'Myapp/Restuarant.html',context)

def cart_detail(request):
    total=0.00
    cart = Cart(request)
    ab=request.session['cart']
    print(ab)

    for key,value in ab.items():
        #print(value['name'])
        total+=(float(value['price'])* float(value['quantity'])) 

    return render(request, 'Myapp/newcart.html',{'total':total})

def cart_add(request, id, resid):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product,restuarantid=resid)
    return redirect("cart_detail")

def item_increment(request, id, resid):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product,restuarantid=resid)
    return redirect("cart_detail")

def item_decrement(request, id, resid):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product,restuarantid=resid)
    return redirect("cart_detail")

def deletecartitem(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product=product)
    return redirect("cart_detail")

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

def ProcessOrder(request):

    add=""
    phn=""
    if request.method=="POST":
        add=request.POST.get('Address')
        phn=request.POST.get('Phone')

    restuarantlist=[]
    ab=request.session['cart']
    for key,value in ab.items():
        if value['restuarantid'] not in restuarantlist:
            restuarantlist.append(value['restuarantid'])

    totals=[]
    sum=0
    for l in restuarantlist:
        for key,value in ab.items():
            if value['restuarantid']==l:
                sum+=float(value['price'])*float(value['quantity'])
        totals.append(sum)
        sum=0

    idx=0
    for res in restuarantlist:
        resid=Restuarant.objects.get(id=res)
        reqobj=Req_info.objects.create(RestuarantID=resid,CustomerID=request.user,status="Pending",GrandTotal=totals[idx],Address=add,Phone=phn)
        idx+=1
        for key,value in ab.items():
            if str(value['restuarantid'])==str(res):
                pid=Product.objects.get(id=value['product_id'])
                OrderDetails.objects.create(orderID=reqobj,FoodID=pid,Foodname=value['name'],FoodSize=value['size'],Foodprice=value['price'],Foodquantity=value['quantity'])
    cart = Cart(request)
    cart.clear()    
    return redirect('index')
#------------end cart------------------
