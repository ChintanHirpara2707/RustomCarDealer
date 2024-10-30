from django.urls import path
from cars import views

urlpatterns = [
    path('', views.cars, name='cars'),
    path('<int:id>/', views.car_detail, name='car_detail'),
    path('search/', views.search, name='search'),
    path('inq_car/', views.inq_car, name='inq_car'),
    path('inquiry/', views.inquiry, name='inquiry'),
    path('dow/', views.dow, name='dow'),


    # URLs for CSV upload and download
    path('upload-csv/', views.CarUploadView.as_view(), name='upload_csv'),
    path('download-csv/', views.CarDownloadView.as_view(), name='download_csv'),

]