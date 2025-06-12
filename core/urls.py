from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('labs/upload/', views.upload_lab, name='upload_lab'),
    path('labs/', views.lab_list, name='lab_list'),
    path('issues/submit/', views.submit_issue, name='submit_issue'),
    path('issues/success/', views.issue_success, name='issue_success'),
    path('consultancy/request/', views.consultancy_request, name='consultancy_request'),
    path('razorpay/payment/verify/', views.razorpay_payment_verify, name='razorpay_payment_verify'),
    path('upload_lab/', views.upload_lab, name='upload_lab'),
    path('labs/', views.labs_view, name='labs_view'),
]