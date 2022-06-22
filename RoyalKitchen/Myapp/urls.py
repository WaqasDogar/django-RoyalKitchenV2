from django.urls import path
from Myapp import views
urlpatterns = [
    path('newindex',views.maintemp,name='newindex'),
    path('',views.template,name='index'),
    path('restuarant/<str:id>',views.restuarant,name='restuarant'),
    path('signin/',views.Login,name='signin'),
    path('signinVendor/',views.signinVendor,name='signinVendor'),
    path('signupVendor/',views.signupVendor,name='signupVendor'),
    path('signup/',views.Signup,name='signup'),
    path('userorder',views.userorder,name='userorder'),
    path('useraccount',views.useraccount,name='useraccount'),
    path('logout', views.Logout, name='logout'),

    path('forget', views.forget , name='forget'),
    path('forgetconfirm', views.forgetconfirm , name='forgetconfirm'),
    
    path('myadmin',views.Login,name='myadmin'),

    #-----cart urls---------------
    path('cart/add/<int:id>/<int:resid>', views.cart_add, name='cart_add'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path('cart/item_increment/<int:id>/<int:resid>',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/<int:resid>',views.item_decrement, name='item_decrement'),
    path('cart/deletecartitem/<int:id>/',views.deletecartitem,name='deletecartitem'),
    path('store', views.ProcessOrder, name='store'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    #------cart completed----------
    path('ResRegistration/',views.ResRegistration,name='ResRegistration'),
    path('Vendor/',views.Vendor,name='Vendor'),
    path('Approve/<int:dataid>/<str:cusid>',views.Approve,name='Approve'),
    path('Reject/<int:dataid>/<str:cusid>',views.Reject,name='Reject'),

    path('Foods/<str:RestID>',views.Foods,name='Foods'),

    path('updatepro/<str:PID>',views.updatepro,name='updatepro'),
    path('deletepro/<str:PID>',views.deletepro,name='deletepro'),
    
    path('Vendorpayments/',views.Vendorpayments,name='Vendorpayments'),
    path('VendorTransaction/',views.VendorTransaction,name='VendorTransaction'),
    path('vendorbilling/', views.vendorbilling, name='vendorbilling'),
    path('Searchindex/<str:searchquerry>',views.Searchindex,name='Searchindex'),

    path('orderstatus/<str:oid>', views.orderstatus, name='orderstatus'),

]