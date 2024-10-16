from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import index, fuel_purchase_record, driver_trip_record, DriverTripRecordListView, FuelPurchaseRecordListView, edit_driver_trip_record, \
    edit_fuel_purchase_record, get_unique_locations, report, delete_driver_trip_record

app_name = 'Routr'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='templates/registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', index, name='index'),
    path('driver_trip_form/', driver_trip_record, name='driver_trip_record'),
    path('fuel_purchase_form/', fuel_purchase_record, name='fuel_purchase_record'),
    path('driver_trip_list/', DriverTripRecordListView.as_view(), name='driver_trip_record_list'),
    path('fuel_purchase_list/', FuelPurchaseRecordListView.as_view(), name='fuel_purchase_record_list'),
    path('driver_trip/edit/<int:pk>/', edit_driver_trip_record, name='edit_driver_trip_record'),
    path('driver_trip/delete/<int:pk>/', delete_driver_trip_record, name='delete_driver_trip_record'),

    path('fuel_purchase/edit/<int:pk>/', edit_fuel_purchase_record, name='edit_fuel_purchase_record'),
    path('get_unique_locations/', get_unique_locations, name='get_unique_locations'),
    path('report/<int:trip_id>/', report, name='report'),

]
