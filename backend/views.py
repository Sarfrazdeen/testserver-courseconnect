from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.timezone import now
from .models import Admission, contactus
from .forms import*
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.views import View 
from datetime import datetime
from django.template.loader import get_template
from xhtml2pdf import pisa
import logging
from django.contrib.auth.models import User
logger = logging.getLogger(__name__)
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Case, When, IntegerField
# Home page view
def webpage(request):
    return render(request, 'index.html')

# Contact page view (with form submission logic)
import logging
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.core.mail import send_mail
from django.utils.timezone import now
from .forms import ContactForm

# Set up logging for debugging
logger = logging.getLogger(__name__)

class ContactUsView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/'  # URL to redirect after a successful submission

    def form_valid(self, form):
        try:
            # Save the form data to the database
            contact = form.save(commit=False)
            contact.save()
            logger.info(f"Contact saved successfully: {contact}")

            # Send email to the client
            self.send_email_to_client(contact)

            # Send email to the admin
            self.send_email_to_admin(contact)

            # Render the success message in the template
            return render(self.request, self.template_name, {
                'form_status': 'success',
            })

        except Exception as e:
            logger.error(f"Error processing form: {e}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        # Log invalid form data for debugging
        logger.warning(f"Form invalid: {form.errors}")
        return render(self.request, self.template_name, {
            'form_status': 'failure',
            'form': form,
        })

    def send_email_to_client(self, contact):
        """
        Sends a thank-you email to the user who submitted the form.
        """
        client_subject = "Thank You for Contacting Us"
        client_message = f"""
        Dear {contact.Full_name},

        Thank you for reaching out to us. We have received your message and will get back to you soon.

        Best regards,
        The Support Team
        """
        client_email = contact.Email
        sender_email = "csesarfraz@gmail.com"

        try:
            send_mail(
                subject=client_subject,
                message=client_message,
                from_email=sender_email,
                recipient_list=[client_email],
                fail_silently=False,
            )
            logger.info(f"Email sent to client: {client_email}")
        except Exception as e:
            logger.error(f"Error sending email to client: {e}")

    def send_email_to_admin(self, contact):
        """
        Sends a notification email to the admin about the new form submission.
        """
        admin_subject = "New Contact Form Submission"
        admin_email = "csesarfraz@gmail.com"
        admin_context = {
            'full_name': contact.Full_name,
            'email': contact.Email,
            'phone_number': contact.Phone_number,
            'message': contact.Message,
            'timestamp': now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # Construct the email body
        admin_message = f"""
        New contact form submission:
        Name: {admin_context['full_name']}
        Email: {admin_context['email']}
        Phone: {admin_context['phone_number']}
        Message: {admin_context['message']}
        Submitted at: {admin_context['timestamp']}
        """

        try:
            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email="csesarfraz@gmail.com",
                recipient_list=[admin_email],
                fail_silently=False,
            )
            logger.info("Email sent to admin")
        except Exception as e:
            logger.error(f"Error sending email to admin: {e}")

# Admission form view
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now
from .forms import AdmissionForm

import logging
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.utils.timezone import now
from django.template.loader import render_to_string
from .forms import AdmissionForm

# Set up logging
logger = logging.getLogger(__name__)

def admission_view(request):
    form_status = None
    error_message = None

    if request.method == 'POST':
        admission_form = AdmissionForm(request.POST)
        if admission_form.is_valid():
            try:
                # Save form data to the database
                admission = admission_form.save()

                # Send email to the client (user)
                try:
                    client_subject = "Thank You for Your Admission Submission"
                    client_message = f"""
                    Dear {admission.full_name},

                    Thank you for submitting your admission form for the {admission.course} course.
                    We have successfully received your information, and our team will contact you soon.

                    Best regards,
                    The Team
                    """
                    send_mail(
                        client_subject,
                        client_message,
                        "csesarfraz@example.com",  # Replace with a valid sender email
                        [admission.email],
                        fail_silently=False,
                    )
                except Exception as client_email_error:
                    logger.error(f"Error sending email to client: {client_email_error}")

                # Send email to the admin
                try:
                    admin_subject = "New Admission Form Submitted"
                    admin_context = {
                        'name': admission.full_name,
                        'email': admission.email,
                        'phone': admission.phone,
                        'course': admission.course,
                        'timestamp': now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    admin_message = render_to_string('admin_email_template.html', admin_context)
                    send_mail(
                        admin_subject,
                        admin_message,
                        "csesarfraz@example.com",  # Replace with a valid sender email
                        ["csesarfraz@example.com"],  # Replace with admin email
                        fail_silently=False,
                        html_message=admin_message,
                    )
                except Exception as admin_email_error:
                    logger.error(f"Error sending email to admin: {admin_email_error}")

                form_status = 'success'
            except Exception as e:
                logger.error(f"Error saving form data: {e}")
                error_message = "An unexpected error occurred while processing your form. Please try again later."
                form_status = 'failure'
        else:
            form_status = 'failure'
            error_message = "There were errors in your submission. Please correct them and try again."
            print(admission_form.errors)  # Log validation errors for debugging

    else:
        admission_form = AdmissionForm()

    return render(
        request,
        'admission_form.html',
        {
            'admission_form': admission_form,
            'form_status': form_status,
            'error_message': error_message,
        }
    )

# List of all admissions (requires login)
@login_required(login_url='/auth/login/')
def admissionlists(request):
    # Ordering the Admissions, making 'finished' status come at the bottom
    all_admissions = Admission.objects.annotate(
        order_status=Case(
            When(status='finished', then=1),
            default=0,
            output_field=IntegerField()
        )
    ).order_by('order_status', '-submission_date')

    context = {'all_admissions': all_admissions}
    return render(request, 'Admissionlist.html', context)


@login_required(login_url='/auth/login/')
def download_pdf(request):
    
    admissions = Admission.objects.all()  # Query all admissions
    template_path = 'admissions_pdf_template.html'  # Create a separate template for the PDF

    context = {
        'admissions': admissions,
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="admissions_list.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)

    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF', content_type='text/plain')
    return response

# Contact list view (requires login)
@login_required(login_url='/auth/login/')
def contactlists(request):
    # Ordering contacts: 'Finished' status comes last, sorted by 'modified_date' descending
    all_contacts = contactus.objects.annotate(
        order_status=Case(
            When(status='Finished', then=1),
            default=0,
            output_field=IntegerField()
        )
    ).order_by('order_status', '-modified_date')

    return render(request, 'Contactlist.html', {'all_contacts': all_contacts})


@login_required(login_url='/auth/login/')
def download_contact_pdf(request):
    # Fetch all contact data
    all_contacts = contactus.objects.all()
    template_path = 'contact_list_pdf.html'  # PDF-specific template

    # Context for the template
    context = {
        'all_contacts': all_contacts,
    }

    # Create an HttpResponse for the PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="contact_list.pdf"'

    # Render the template into HTML
    template = get_template(template_path)
    html = template.render(context)

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Check for errors during PDF generation
    if pisa_status.err:
        return HttpResponse('Error generating PDF', content_type='text/plain')

    return response

# Delete contact (requires login)
@login_required(login_url='/auth/login/')
def deletecontacts(request, id):
    del_contacts = contactus.objects.get(id=id)
    del_contacts.delete()
    return redirect('Contactlist')

# Update contact (requires login)
@login_required(login_url='/auth/login/')
def updatecontacts(request, id):
    up_contacts = get_object_or_404(contactus, id=id)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=up_contacts)
        if form.is_valid():
            form.save()
            return redirect('Contactlist')
    else:
        form = ContactForm(instance=up_contacts)

    return render(request, 'contact.html', {'contact_form': form})

# Update admission (requires login)
@login_required(login_url='/auth/login/')
def updateadmission(request, id):
    admission_to_update = get_object_or_404(Admission, id=id)

    if request.method == 'POST':
        form = AdmissionForm(request.POST, instance=admission_to_update)
        if form.is_valid():
            form.save()
            return redirect('Admissionlist')
    else:
        form = AdmissionForm(instance=admission_to_update)

    return render(request, 'updateadmission.html', {'admission_form': form})

# Delete admission (requires login)
@login_required(login_url='/auth/login/')
def deleteadmission(request, id):
    admission_to_delete = Admission.objects.get(id=id)
    admission_to_delete.delete()
    return redirect('Admissionlist')  # Redirect after deletion

# Admin dashboard (requires login)
@login_required(login_url='/auth/login/')
def adminboard(request):
    return render(request, 'admindashboard.html')

# Admission Form View to handle form submission and pre-filled data
class CourseListView(View):
    template_name = 'courselist.html'

    def get(self, request, *args, **kwargs):
        courses = [
            {'name': 'C Programming', 'duration': '1 Month'},
            {'name': 'Python Programming', 'duration': '45 Days'},
            {'name': 'Java Programming', 'duration': '2 Months'},
            {'name': 'Full Stack Development (Python)', 'duration': '3 Months'},
            {'name': 'React JS', 'duration': '1 Month'},
            {'name': 'Front-End Web Development', 'duration': '1.5 Months'},
            {'name': 'AutoCAD', 'duration': '1 Month'},
            {'name': 'Revit', 'duration': '2 Months'},
            {'name': 'Civil 3D', 'duration': '3 Months'},
            {'name': 'Digital Marketing', 'duration': '2 Months'},
        ]
        return render(request, self.template_name, {'courses': courses})

class AdmissionFormView(View):
    template_name = 'admission_form2.html'

    def get(self, request, *args, **kwargs):
        print(request.POST)
        selected_course = request.GET.get('course', '')
        course_duration = request.GET.get('duration', '')

        # Initialize the form with the selected course if it's provided in the GET parameters
        form = AdmissionForm(initial={'course': selected_course}) 
        return render(request, self.template_name, {
            'form': form,
            'course_name': selected_course,
            'course_duration': course_duration,
        })

    def post(self, request, *args, **kwargs):
        selected_course = request.GET.get('course', '') 
        course_duration = request.GET.get('duration', '')

        # Ensure that the 'course' field is included in the POST data
        if selected_course:
            request.POST = request.POST.copy() 
            request.POST['course'] = selected_course 

        form = AdmissionForm(request.POST)

        if form.is_valid():
            # Save form data to the database
            admission = form.save()

            # Send email to the client (user)
            client_subject = "Thank You for Your Admission Submission"
            client_message = f"""
            Dear {admission.full_name},

            Thank you for submitting your admission form for the {admission.course} course.
            We have successfully received your information, and our team will contact you soon.

            Best regards,
            The Team
            """
            client_email = admission.email
            sender_email = "csesarfraz@example.com"
            send_mail(
                client_subject,
                client_message,
                sender_email,
                [client_email],
                fail_silently=False,
            )

            # Send email to the admin
            admin_subject = "New Admission Form Submitted"
            admin_email = "csesarfraz@example.com"
            admin_context = {
                'name': admission.full_name,
                'email': admission.email,
                'phone': admission.phone,
                'course': admission.course,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            admin_message = render_to_string('admin_email_template.html', admin_context)
            send_mail(
                admin_subject,
                admin_message,
                sender_email,
                [admin_email],
                fail_silently=False,
                html_message=admin_message,
            )

            # Display success message and redirect
            messages.success(request, "Your admission form has been successfully submitted!")
            return redirect('home') 

        else:
            return render(request, self.template_name, {
                'form': form,
                'course_name': selected_course,
                'course_duration': course_duration,
            })
        
User = get_user_model()
        

@login_required(login_url='/auth/login/')
def update_status_cont(request, id):
    if request.method == "POST":
        try:
            # Fetch the contact record by ID
            contact = contactus.objects.get(id=id)
            
            # Update status and modified_date
            contact.status = request.POST.get('status')
            contact.updated_by_id = request.POST.get('admin_id')  # Admin ID
            contact.modified_date = now()  # Set the modified date
            
            contact.save()  # Save changes to the database
            messages.success(request, "Status updated successfully!")
        except contactus.DoesNotExist:
            messages.error(request, "Contact not found!")
        
        return redirect('Contactlist')

@login_required(login_url='/auth/login/')
def update_admission_status(request, admission_id):
    if request.method == 'POST':
        admission = get_object_or_404(Admission, id=admission_id)
        new_status = request.POST.get('status')
        admin_id = request.POST.get('admin_id')

        # Update admission details
        admission.status = new_status
        admission.modified_by = admin_id
        admission.modified_date = now()
        admission.save()

        return redirect('admission_list')

    return HttpResponse("Invalid Request", status=400)

@login_required(login_url='/auth/login/')
def update_status(request, admission_id):
    admission = get_object_or_404(Admission, id=admission_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        admission.status = new_status
        admission.modified_by_user_id = request.user.id  # Set the modified_by_user_id to the logged-in user's ID
        admission.save()
        messages.success(request, 'Status updated successfully.')
    return redirect('Admissionlist')

@login_required(login_url='/auth/login/')
def add_admission(request):
    if request.method == 'POST':
        form = AdmissionForm(request.POST)
        print('POST Data:', request.POST)  # Debugging POST data
        if form.is_valid():
            try:
                admission = form.save(commit=False)
                print('User ID:', request.user.id)  # Debugging user ID
                admission.created_by_user_id = request.user.id
                admission.save()
                messages.success(request, 'Admission added successfully.')
                print('Redirecting to:', reverse('Admissionlist'))  # Debugging redirect
                return redirect('Admissionlist')
            except Exception as e:
                print('Error while saving admission:', e)  # Debugging error
                messages.error(request, 'An unexpected error occurred.')
        else:
            print('Form errors:', form.errors)  # Debugging form errors
            messages.error(request, 'Please correct the errors in the form.')
    return redirect('Admissionlist')

@login_required(login_url='/auth/login/')
def admission_list(request):
    # Access the choices from the Admission model
    course_choices = Admission.COURSE_CHOICES

    all_admissions = Admission.objects.all()

    # Make sure the choices are correctly passed
    context = {
        'course_choices': course_choices,  # Passing course choices to the template
        'all_admissions': all_admissions,
    }

    return render(request, 'admission_list.html', context)


    