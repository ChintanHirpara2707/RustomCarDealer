from urllib import request
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.html import format_html
from django.contrib import messages
import csv
import io
from .models import Car

class CarAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(object.car_photo.url))

    thumbnail.short_description = 'Car Image'
    list_display = ('id', 'thumbnail', 'car_title', 'city', 'color', 'model', 'year', 'body_style', 'fuel_type', 'is_featured')
    list_display_links = ('id', 'thumbnail', 'car_title')
    list_editable = ('is_featured',)
    search_fields = ('id', 'car_title', 'city', 'model', 'body_style', 'fuel_type')
    list_filter = ('city', 'model', 'body_style', 'fuel_type')

    # Method to handle CSV download
    def download_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="cars.csv"'
        writer = csv.writer(response)

        # Write header row
        writer.writerow([
            'Car Title', 'State', 'City', 'Color', 'Model', 'Year', 'Condition', 'Price',
            'Description', 'Car Photo', 'Car Photo 1', 'Car Photo 2', 'Car Photo 3', 'Car Photo 4',
            'Features', 'Body Style', 'Engine', 'Transmission', 'Interior', 'Miles', 'Doors',
            'Passengers', 'VIN No', 'Mileage', 'Fuel Type', 'No of Owners', 'Created Date'
        ])

        # Write data rows
        cars = Car.objects.all().values_list(
            'car_title', 'state', 'city', 'color', 'model', 'year', 'condition', 'price',
            'description', 'car_photo', 'car_photo_1', 'car_photo_2', 'car_photo_3', 'car_photo_4',
            'features', 'body_style', 'engine', 'transmission', 'interior', 'miles', 'doors',
            'passengers', 'vin_no', 'milage', 'fuel_type', 'no_of_owners', 'created_date'
        )

        for car in cars:
            car_data = list(car)
            car_data[14] = '|'.join(car_data[14])  # Convert features from list to string
            writer.writerow(car_data)

        return response

    download_csv.short_description = 'Download CSV'

    # Method to handle CSV upload
    def upload_csv(self, request):
        if request.method == 'POST' and request.FILES.get('csv_file'):
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return redirect('admin:cars_car_changelist')

            # Read and process CSV file
            file_data = csv_file.read()

            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'windows-1252']
            io_string = None
            for enc in encodings:
                try:
                    io_string = io.StringIO(file_data.decode(enc))
                    break
                except UnicodeDecodeError:
                    continue

            if io_string is None:
                messages.error(request, 'Unable to decode file. Please check the encoding.')
                return redirect('admin:cars_car_changelist')

            reader = csv.reader(io_string)
            next(reader)  # Skip header row

            # Track row number for debugging
            row_number = 0

            for row in reader:
                row_number += 1
                if len(row) != 27:  # Adjust this number based on the actual number of columns in your CSV
                    messages.error(request, f'Skipping row {row_number}: Incorrect number of columns')
                    continue

                try:
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
                except IndexError as e:
                    messages.error(request, f'Error processing row {row_number}: {e}')
                    continue

            messages.success(request, 'CSV file has been uploaded successfully.')
            return redirect('admin:cars_car_changelist')

        # Handle GET request to display the upload form
        return render(request, 'admin/upload_csv.html')


    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('upload-csv/', self.admin_site.admin_view(self.upload_csv), name='upload_csv'),
            path('download-csv/', self.admin_site.admin_view(self.download_csv), name='download_csv'),
        ]
        return custom_urls + urls

    actions = []

admin.site.register(Car, CarAdmin)
