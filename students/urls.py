from django.conf.urls import url

from . import views

# Added for accessing URLs using their name
app_name = 'students'

urlpatterns = [
    
    # Open register page by default
    url(r'^$', views.register, name='index'),

    # Form for user inputs
    url(r'^register/', views.register, name='register'),
    
	# Form for verifying the mobile number during registration
    url(r'^verify/', views.verify, name='verify'),

    url(r'^submit/', views.submit, name='submit'),
    url(r'^info_show/', views.info_show, name='info_show'),
    
    url(r'^success/', views.success, name='success'),

    # Enter phone number to view registered classes
    url(r'^info/get/', views.info_get, name='info_get'),
]