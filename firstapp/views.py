from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login as auth_login, logout as auth_logout
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from .models import userRegister, Car, TestDrive
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomUserChangeForm, CarForm, ContactForm, CustomerReviewForm
import csv
import os
import shutil
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import Http404, HttpResponse, HttpResponseBadRequest


from django.shortcuts import render
from .models import userRegister  # Adjust this import according to your actual model name and location

def profile_view(request):
    users = userRegister.objects.all()  # Fetch all users
    return render(request, 'prof.html', {'users': users})

def proadm_view(request):
    users = userRegister.objects.all()  # Fetch all users
    return render(request, 'proadm.html', {'users': users})

from django.shortcuts import get_object_or_404, redirect
from .models import userRegister

def delete_user(request, user_id):
    user = get_object_or_404(userRegister, id=user_id)
    user.delete()
    return redirect('prof')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect(request.POST.get('next', 'index'))  # Redirect to the next page or index
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def adm_registration(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        phone = request.POST['phone']
        branch = request.POST['branch']

        if userRegister.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'admregister.html')

        if userRegister.objects.filter(email=email).exists():
            messages.error(request, 'Email ID already exists')
            return render(request, 'admregister.html')

        # Create the user with hashed password
        user = userRegister(
            username=username,
            password=make_password(password),
            email=email,
            phone=phone,
            branch=branch
        )
        user.save()

        # Send registration confirmation email
        subject = 'Welcome to RUSTOM Store'
        html_message = render_to_string('email.html', {'first_name': username})
        plain_message = strip_tags(html_message)
        from_email = 'chintanhirpara005@gmail.com'  # Ensure this email is set up correctly in your settings
        to = email
        recipient_list = [email]
        
        try:
            send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
            messages.success(request, 'Registration successful! A confirmation email has been sent.')
        except Exception as e:
            messages.error(request, f'Registration successful but failed to send email: {e}')

        return redirect('admlogin')
    
    return render(request, 'admregister.html')

def process_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = userRegister.objects.get(email=email)
            if check_password(password, user.password):
                request.session['username'] = user.username
                messages.success(request, 'Login successful')
                return redirect('index')  # Redirect to index view
            else:
                messages.error(request, 'Invalid login credentials')
        except userRegister.DoesNotExist:
            messages.error(request, 'Invalid login credentials')

    return render(request, 'login.html')  # Render login page if login fails

def logout_view(request):
    auth_logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect('admlogin')

def index(request):
    return render(request, 'index.html', {'username': request.user.username})

def test_drive(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        date = request.POST['date']
        car_model = request.POST['car_model']

        # Save the data to the database
        TestDrive.objects.create(
            name=name,
            email=email,
            phone=phone,
            date=date,
            car_model=car_model
        )

        # Redirect to a thank you or confirmation page (optional)
        return redirect('thank_you')

    return render(request, 'test_drive.html')


def thank_you(request):
    return render(request, 'thank_you.html')

def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save()  # Save the form data to the database
            # Redirect to view_car page for the newly created car
            return redirect('car_detail', pk=car.pk)  # Redirect to car_detail page
    else:
        form = CarForm()
    return render(request, 'add_car.html', {'form': form})

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()  # Save updated form data to the database
            return redirect('car_detail', pk=car.pk)  # Redirect to view updated car details
    else:
        form = CarForm(instance=car)

    return render(request, 'car_detail.html', {'car': car, 'form': form})

def view_all_cars(request):
    cars = Car.objects.all()
    return render(request, 'view_all_cars.html', {'cars': cars})

def update_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_detail', pk=pk)
    else:
        form = CarForm(instance=car)
    return render(request, 'update_car.html', {'form': form})

def delete_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    car.delete()
    return redirect('view_all_cars')

def about_us(request):
    return render(request, 'about_us.html')

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the index view
    else:
        form = ContactForm()

    return render(request, 'contact_us.html', {'form': form})

def customer_review(request):
    if request.method == "POST":
        form = CustomerReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Adjust with your URL name
    else:
        form = CustomerReviewForm()
    
    return render(request, 'customer_review.html', {'form': form})

def upload_csv(request):
    if request.method == "POST":
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'This is not a CSV file')
            return redirect('view_all_cars')
        if csv_file.multiple_chunks():
            messages.error(request, 'Uploaded file is too big')
            return redirect('view_all_cars')

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split('\n')
        for line in lines[1:]:  # Skip the header line
            if line.strip():  # Skip any empty lines
                fields = line.split(",")
                car_name = fields[0]
                car_model = fields[1]
                car_engine = fields[2]
                car_power = fields[3]
                seating_capacity = fields[4]
                transmission = fields[5]
                car_image_path = fields[6]

                # Copy image to media directory
                image_name = os.path.basename(car_image_path.strip())  # Extract the image file name
                destination_path = os.path.join(settings.MEDIA_ROOT, 'car_images', image_name)
                
                # Create the directory if it doesn't exist
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                
                # Copy the file
                try:
                    shutil.copy(car_image_path.strip(), destination_path)
                except IOError as e:
                    messages.error(request, f'Error copying file: {car_image_path}. Error: {e}')
                    return redirect('view_all_cars')

                # Ensure the path is relative to the media directory
                car_image = os.path.join('car_images', image_name)

                # Create and save the Car object
                Car.objects.create(
                    car_name=car_name,
                    car_model=car_model,
                    car_engine=car_engine,
                    car_power=car_power,
                    seating_capacity=seating_capacity,
                    transmission=transmission,
                    car_image=car_image
                )

        messages.success(request, 'CSV file successfully uploaded and data added')
        return redirect('view_all_cars')
    return render(request, 'upload_csv.html')

def download_csv(request):
    # Create the HttpResponse object with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cars.csv"'

    writer = csv.writer(response)
    writer.writerow(['Car Name', 'Car Model', 'Car Engine', 'Car Power', 'Seating Capacity', 'Transmission', 'Car Image'])

    cars = Car.objects.all()
    for car in cars:
        writer.writerow([
            car.car_name,
            car.car_model,
            car.car_engine,
            car.car_power,
            car.seating_capacity,
            car.transmission,
            car.car_image.url  # Assuming car_image is a FileField or ImageField
        ])

    return response

def download_file(request):
    file_path = 'path/to/your/file.csv'  # Update this path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
    raise Http404

