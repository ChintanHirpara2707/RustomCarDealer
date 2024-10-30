from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import EmailMessage ,EmailMultiAlternatives
from .forms import OTPForm
import random
import string

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(user_email, otp):
    subject = 'Your Password Reset OTP'
    message = f'Your OTP is: {otp}'
    from_email = 'chintanhirpara005@gmail.com' 
    send_mail(subject, message, from_email, [user_email])

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email address.')
            return redirect('password_reset')
        
        otp = generate_otp()
        request.session['otp'] = otp
        request.session['email'] = email 
        send_otp_email(email, otp)
        messages.success(request, 'An OTP has been sent to your email.')
        return redirect('password_reset_otp')
    
    return render(request, 'accounts/password_reset.html')

def password_reset_otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            new_password = form.cleaned_data['new_password']

            if otp == request.session.get('otp'):
                user = User.objects.get(email=request.session.get('email'))
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('login')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = OTPForm()

    return render(request, 'accounts/password_reset_otp.html', {'form': form})

def send_otp_email(user_email, otp):
    """Send OTP via email with HTML template"""
    subject = 'Your Password Reset OTP'
    html_message = render_to_string('otp_email.html', {'otp': otp})
    plain_message = strip_tags(html_message)
    
    from_email = 'chintanhirpara005@gmail.com'
    email = EmailMultiAlternatives(
        subject,
        plain_message,
        from_email,
        [user_email]
    )
    
    email.attach_alternative(html_message, "text/html") 
    email.send()

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password)
                    user.save()
                    subject = 'Welcome to RUSTOM Store'
                    html_message = render_to_string('email.html', {'username': firstname})
                    plain_message = strip_tags(html_message)
                    from_email = 'chintanhirpara005@gmail.com'
                    recipient_list = [email]
                    
                    try:
                        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
                        messages.success(request, 'You are registered successfully. A confirmation email has been sent.')
                    except Exception as e:
                        messages.error(request, f'Registration successful but failed to send email: {e}')
                    
                    auth.login(request, user)
                    return redirect('dashboard')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

@login_required(login_url='login')
def profile(request):
    user = request.user

    password_change_form = PasswordChangeForm(user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')

            if first_name and last_name and username and email:
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email

                try:
                    user.save()
                    messages.success(request, 'Profile updated successfully.')
                except Exception as e:
                    messages.error(request, f'Profile update failed: {e}')
            else:
                messages.error(request, 'Please fill out all required fields for profile update.')

        elif 'change_password' in request.POST:
            
            password_change_form = PasswordChangeForm(user, request.POST)
            if password_change_form.is_valid():
                password_change_form.save()
                update_session_auth_hash(request, password_change_form.user)
                messages.success(request, 'Password changed successfully.')
            else:
                for error in password_change_form.errors.values():
                    messages.error(request, error)

    return render(request, 'accounts/profile.html', {
        'password_change_form': password_change_form,
        'user': user,
    })


@login_required(login_url = 'login')
def dashboard(request):
    user_inquiry = Contact.objects.order_by('-create_date').filter(user_id=request.user.id)

    data = {
        'inquiries': user_inquiry,
    }
    return render(request, 'accounts/dashboard.html', data)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return redirect('home')
