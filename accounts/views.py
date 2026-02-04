from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import ProfileUpdateForm
import requests

def register_view(request):
    if request.method == 'POST':
        u = request.POST['username']
        e = request.POST['email']
        p = request.POST['password']

        if User.objects.filter(username=u).exists():
            messages.error(request, "Username already exists")
        elif User.objects.filter(email=e).exists():
            messages.error(request, "Email already used")
        elif len(p) < 8:
            messages.error(request, "Password must be at least 8 characters")
        else:
            User.objects.create_user(username=u, email=e, password=p)
            messages.success(request, "Registered successfully. Login now.")
            return redirect('login')

    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, "Invalid credentials")
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def settings_view(request):
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('settings')
        
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important to keep the user logged in
                messages.success(request, "Password changed successfully!")
                return redirect('settings')
            else:
                messages.error(request, "Please correct the error below.")
    
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'accounts/settings.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })

def get_location_from_pincode(pincode):
    if not pincode:
        return None
    try:
        url = f"https://api.postalpincode.in/pincode/{pincode}"
        response = requests.get(url, timeout=5)
        data = response.json()
        if data[0]['Status'] == 'Success':
            # Get the first post office name and district
            post_office = data[0]['PostOffice'][0]
            return f"{post_office['Name']}, {post_office['District']}"
    except Exception as e:
        print(f"Error fetching location: {e}")
    return None

import secrets
import string
from django.core.mail import send_mail

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate random 8-char password
            alphabet = string.ascii_letters + string.digits
            otp = ''.join(secrets.choice(alphabet) for i in range(8))
            
            user.set_password(otp)
            user.save()
            
            # Send Email
            subject = 'Password Reset - Citizen First'
            message = f'Your one-time password is: {otp}\n\nPlease login and change your password in settings immediately.'
            email_from = 'admin@citizenfirst.com'
            recipient_list = [email]
            
            # print(f"DEBUG OTP for {email}: {otp}") # REMOVED FOR SECURITY
            
            try:
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)
                messages.success(request, f"One-Time Password sent to {email}")
            except Exception as e:
                print(f"Email sending failed: {e}")
                messages.warning(request, "Email sending failed. Please try again later or contact support.")
                
            return redirect('login')
            
        except User.DoesNotExist:
            messages.error(request, "No account found with this email")
            
    return render(request, 'accounts/forgot_password.html')
