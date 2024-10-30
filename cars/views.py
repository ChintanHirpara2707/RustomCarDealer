from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
import csv
import io
from .models import Car
from django.views import View
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Inquiry

# Existing views
def cars(request):
    cars = Car.objects.order_by('-created_date')
    paginator = Paginator(cars, 4)
    page = request.GET.get('page')
    paged_cars = paginator.get_page(page)

    model_search = Car.objects.values_list('model', flat=True).distinct()
    city_search = Car.objects.values_list('city', flat=True).distinct()
    year_search = Car.objects.values_list('year', flat=True).distinct()
    body_style_search = Car.objects.values_list('body_style', flat=True).distinct()

    data = {
        'cars': paged_cars,
        'model_search': model_search,
        'city_search': city_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
    }
    return render(request, 'cars/cars.html', data)


def car_detail(request, id):
    single_car = get_object_or_404(Car, pk=id)

    data = {
        'single_car': single_car,
    }
    return render(request, 'cars/car_detail.html', data)


def inq_car(request):
    return render(request, 'cars/inq_car.html')


def search(request):
    cars = Car.objects.order_by('-created_date')

    model_search = Car.objects.values_list('model', flat=True).distinct()
    city_search = Car.objects.values_list('city', flat=True).distinct()
    year_search = Car.objects.values_list('year', flat=True).distinct()
    body_style_search = Car.objects.values_list('body_style', flat=True).distinct()
    transmission_search = Car.objects.values_list('transmission', flat=True).distinct()

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            cars = cars.filter(description__icontains=keyword)

    if 'model' in request.GET:
        model = request.GET['model']
        if model:
            cars = cars.filter(model__iexact=model)

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            cars = cars.filter(city__iexact=city)

    if 'year' in request.GET:
        year = request.GET['year']
        if year:
            cars = cars.filter(year__iexact=year)

    if 'body_style' in request.GET:
        body_style = request.GET['body_style']
        if body_style:
            cars = cars.filter(body_style__iexact=body_style)

    if 'min_price' in request.GET:
        min_price = request.GET['min_price']
        max_price = request.GET['max_price']
        if max_price:
            cars = cars.filter(price__gte=min_price, price__lte=max_price)

    data = {
        'cars': cars,
        'model_search': model_search,
        'city_search': city_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
        'transmission_search': transmission_search,
    }
    return render(request, 'cars/search.html', data)


# New views for CSV upload and download
class CarUploadView(View):
    def post(self, request, *args, **kwargs):
        if request.FILES.get('csv_file'):
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return redirect('admin:cars_car_changelist')

            file_data = csv_file.read().decode('utf-8')
            io_string = io.StringIO(file_data)
            reader = csv.reader(io_string)
            next(reader)  # Skip header row

            for row in reader:
                _, created = Car.objects.update_or_create(
                    car_title=row[0],
                    defaults={
                        'state': row[1],
                        'city': row[2],
                        'color': row[3],
                        'model': row[4],
                        'year': row[5],
                        'condition': row[6],
                        'price': row[7],
                        'description': row[8],
                        'car_photo': row[9],
                        'car_photo_1': row[10],
                        'car_photo_2': row[11],
                        'car_photo_3': row[12],
                        'car_photo_4': row[13],
                        'features': row[14].split('|'),
                        'body_style': row[15],
                        'engine': row[16],
                        'transmission': row[17],
                        'interior': row[18],
                        'miles': row[19],
                        'doors': row[20],
                        'passengers': row[21],
                        'vin_no': row[22],
                        'milage': row[23],
                        'fuel_type': row[24],
                        'no_of_owners': row[25],
                        'created_date': row[26],
                    }
                )

            messages.success(request, 'CSV file has been uploaded successfully.')
        return redirect('admin:cars_car_changelist')

    def get(self, request, *args, **kwargs):
        return HttpResponse('GET method not allowed.')


class CarDownloadView(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=cars.csv'

        writer = csv.writer(response)
        writer.writerow([
            'car_title', 'state', 'city', 'color', 'model', 'year', 'condition',
            'price', 'description', 'car_photo', 'car_photo_1', 'car_photo_2',
            'car_photo_3', 'car_photo_4', 'features', 'body_style', 'engine',
            'transmission', 'interior', 'miles', 'doors', 'passengers', 'vin_no',
            'milage', 'fuel_type', 'no_of_owners', 'created_date'
        ])

        cars = Car.objects.all().values_list(
            'car_title', 'state', 'city', 'color', 'model', 'year', 'condition',
            'price', 'description', 'car_photo', 'car_photo_1', 'car_photo_2',
            'car_photo_3', 'car_photo_4', 'features', 'body_style', 'engine',
            'transmission', 'interior', 'miles', 'doors', 'passengers', 'vin_no',
            'milage', 'fuel_type', 'no_of_owners', 'created_date'
        )
        for car in cars:
            writer.writerow(car)

        return response

def dow(request):
    return render(request, 'cars/dow.html') 

# PDF generation logic
def generate_pdf(inquiry, car):
    template_path = 'invoice.html'
    context = {
        'inquiry': inquiry,
        'car': car,
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    template = get_template(template_path)
    html_string = template.render(context)
    pisa_status = pisa.CreatePDF(html_string, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)

    return response


# Inquiry view
def inquiry(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        car_id = request.POST.get('car_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        customer_need = request.POST.get('customer_need')
        city = request.POST.get('city')
        state = request.POST.get('state')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        car = Car.objects.get(id=car_id)

        inquiry = Inquiry(
            user_id=user_id,
            car_id=car_id,
            first_name=first_name,
            last_name=last_name,
            customer_need=customer_need,
            city=city,
            state=state,
            email=email,
            phone=phone,
            message=message,
        )
        inquiry.save()

        return generate_pdf(inquiry, car)

    return redirect('car_detail', id=car_id)