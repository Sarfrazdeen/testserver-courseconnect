from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

# Login view
def user_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')  # Redirect to the admin dashboard if already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')  # Redirect to the admin dashboard
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')  # Redirect to login page

    return render(request, 'Login.html')

# Logout view
def user_logout(request):
    logout(request)  # Log the user out
    messages.success(request, "You have been logged out successfully.")

    # Redirect to home page instead of login
    response = HttpResponseRedirect(reverse('home'))  # Redirect to home page
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response  # Send response with headers to prevent caching
