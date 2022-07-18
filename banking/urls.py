from django.contrib import admin
from django.urls import path
from banking import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path("", views.index, name='index'),
    path("contact", views.contact, name='contact'),
    path('register/', views.register, name='register'),
	path('login/',views.login, name="login"),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('logout', views.logout, name='logout'),
    path('customer/', views.customer, name='customer'),
    path('operation/', views.operation, name='operation'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
    path('txn/', views.trans, name='txn'),
    path('atm/', views.atm, name='atm'),
    path('viewcustomer/', views.viewcustomer, name='viewcustomer'),
    path('transfer/', views.transfer, name='transfer'),
    path('applyforloan/', views.applyforloan, name='applyforloan'),
    path('loanapproval/', views.loanapproval, name='loanapproval'),
    path('viewtransfer/', views.viewtransfer, name='viewtransfer'),
    path('atmcard/', views.atmcard, name='atmcard'),
    path('emiview/', views.emiview, name='emiview'),
    path('emi/', views.emi, name='emi'),
    
    
]