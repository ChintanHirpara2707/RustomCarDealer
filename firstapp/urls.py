from firstapp import views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login_view, name='admlogin'),
    path('adm_registration/', views.adm_registration, name="admregister"),
    path('prof/', views.profile_view, name='prof'),
    path('proadm/', views.proadm_view, name='proadm'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('process_login/', views.process_login, name="process_login"),
    path('add_car/', views.add_car, name='add_car'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('view_all_cars/', views.view_all_cars, name='view_all_cars'),
    path('logout/', views.logout_view, name='logout_view'),     
    path('index/', views.index, name="index"),
    path("test_drive/", views.test_drive, name="test_drive"),
    path('update_car/<int:pk>/', views.update_car, name='update_car'),
    path('delete_car/<int:pk>/', views.delete_car, name='delete_car'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('about_us/', views.about_us, name='about_us'),
    path('customer_review/', views.customer_review, name='customer_review'),
    path('upload_csv/', views.upload_csv, name="upload_csv"),
    path('download_csv/', views.download_csv, name='download_csv'),
    path('thank_you/', views.thank_you, name='thank_you'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
