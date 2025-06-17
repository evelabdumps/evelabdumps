from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),  # Root URL for landing page
    path('home/', views.home, name='home'),  # Separate home URL
    path('labs/upload/', views.upload_lab, name='upload_lab'),  # Upload labs
    path('labs/images/upload/', views.upload_lab_image, name='upload_lab_image'),  # Upload images for labs
    path('labs/list/', views.lab_list, name='lab_list'),  # List labs
    path('labs/view/', views.labs_view, name='labs_view'),  # View labs
    path('issues/submit/', views.submit_issue, name='submit_issue'),  # Submit issues
    path('issues/success/', views.issue_success, name='issue_success'),  # Success page for issues
    path('consultancy/request/', views.consultancy_request, name='consultancy_request'),  # Consultancy request
    path('razorpay/payment/verify/', views.razorpay_payment_verify, name='razorpay_payment_verify'),  # Payment verification
    path('images/', views.image_gallery, name='image_gallery'),
]
