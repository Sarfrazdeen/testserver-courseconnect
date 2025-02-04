from django.urls import path
from . import views  # Import the views from your backend app

urlpatterns = [
    # Home page
    path('', views.webpage, name='home'),

    # Contact form view
    path('contact/', views.ContactUsView.as_view(), name='contact_us'),

    # Admission form view (for adding new admission)
    path('admissions/add/', views.admission_view, name='admission_view'),

    # List of all admissions
    path('admissions/', views.admissionlists, name='Admissionlist'),

    # Contact list view (only accessible if logged in)
    path('contacts/', views.contactlists, name='Contactlist'),

    # Delete contact by ID
    path('contacts/delete/<int:id>/', views.deletecontacts, name='delete_contacts'),

    # Update contact by ID
    path('contacts/update/<int:id>/', views.updatecontacts, name='update_contacts'),

    # Update admission by ID
    path('admissions/update/<int:id>/', views.updateadmission, name='updateadmission'),

    # Delete admission by ID
    path('admissions/delete/<int:id>/', views.deleteadmission, name='deleteadmission'),

    # Admin dashboard view (only accessible if logged in)
    path('adminboard/', views.adminboard, name='admin_dashboard'),

    # Course list page (new view for displaying courses)
     path('courselist/', views.CourseListView.as_view(), name='course_list'),  # This is for the course list view

    # Admission form view (for enrolling in courses)
    path('admission-formtwo/', views.AdmissionFormView.as_view(), name='admission_form'),

     path('download_admissions/', views.download_pdf, name='download_admissions'),

     path('download-contact-pdf/', views.download_contact_pdf, name='download_contact_pdf'),

     path('contact/update_status/<int:id>/', views.update_status_cont, name='update_status_cont'),

     path('admissions/update/<int:admission_id>/', views.update_admission_status, name='update_admission_status'),

     path('admin/admissions/add/', views.add_admission, name='add_admission2'),

     path('admissions/update_status/<int:admission_id>/', views.update_status, name='update_status'),

     path('admission-list/', views.admission_list, name='admission_list'),

     
    ]
