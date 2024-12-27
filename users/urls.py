from django.contrib.auth import views as auth_views
from django.urls import path
from .views import ProfileView  # Ensure this import is present


app_name = 'users'  # Add the namespace here

urlpatterns = [
    
   
    
  
path('profile/', ProfileView.as_view(), name='profile'),
 
    

]







