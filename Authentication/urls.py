from django.urls import path
from .views import*  # Import views from the Authentication app

urlpatterns = [
    # Login page for the authenticate app
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('admin/', render, {'template_name': 'admindashboard.html'}, name='admin_dashboard')
    
]
