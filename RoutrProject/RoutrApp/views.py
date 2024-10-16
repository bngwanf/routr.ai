from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.views.decorators.cache import cache_page
from django.views.generic import ListView

from .forms import DriverTripRecordForm, FuelPurchaseRecordForm, StopFormSet
from .gpt_utils import OpenAICompletionClient
from .models import DriverTripRecord, FuelPurchaseRecord, Stop


# Create your views here.



@login_required
def index(request):
    return render(request, 'index.html')


class DriverTripRecordListView(LoginRequiredMixin, ListView):
    model = DriverTripRecord
    template_name = 'driver_trip_record_list.html'
    context_object_name = 'driver_trip_records'
    paginate_by = 10  # Number of records per page
    ordering = ['id']


@login_required
def driver_trip_record(request):
    if request.method == 'POST':
        form = DriverTripRecordForm(request.POST)
        formset = StopFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            trip_record = form.save()
            formset.instance = trip_record
            formset.save()
            return redirect('Routr:driver_trip_record_list')
    else:
        form = DriverTripRecordForm()
        formset = StopFormSet()
    return render(request, 'driver_trip_record.html', {'form': form, 'formset': formset})


@login_required
def edit_driver_trip_record(request, pk):
    record = get_object_or_404(DriverTripRecord, pk=pk)
    if request.method == 'POST':
        form = DriverTripRecordForm(request.POST, instance=record)

        formset = StopFormSet(request.POST, instance=record)
        # print(form.errors)
        print(formset.errors)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('Routr:driver_trip_record_list')
    else:
        form = DriverTripRecordForm(instance=record)
        formset = StopFormSet(instance=record)
    return render(request, 'driver_trip_record.html', {'form': form, 'formset': formset})


@login_required
def delete_driver_trip_record(request, pk):
    record = get_object_or_404(DriverTripRecord, pk=pk)
    record.delete()
    messages.success(request, 'Driver trip record deleted successfully.')
    return redirect('Routr:driver_trip_record_list')

###############################################################################################################

class FuelPurchaseRecordListView(LoginRequiredMixin, ListView):
    model = FuelPurchaseRecord
    template_name = 'fuel_purchase_record_list.html'
    context_object_name = 'fuel_purchase_records'
    paginate_by = 10  # Number of records per page
    ordering = ['id']


@login_required
def fuel_purchase_record(request):
    if request.method == 'POST':
        form = FuelPurchaseRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Routr:fuel_purchase_record_list')
    else:
        form = FuelPurchaseRecordForm()
    return render(request, 'fuel_purchase_record.html', {'form': form})


@login_required
def edit_fuel_purchase_record(request, pk):
    record = get_object_or_404(FuelPurchaseRecord, pk=pk)
    if request.method == 'POST':
        form = FuelPurchaseRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('Routr:fuel_purchase_record_list')
    else:
        form = FuelPurchaseRecordForm(instance=record)
    return render(request, 'fuel_purchase_record.html', {'form': form})


@login_required
def get_unique_locations(request):
    query = request.GET.get('q', '')
    starting_locations = DriverTripRecord.objects.filter(starting_location__icontains=query).values_list('starting_location', flat=True).distinct()
    ending_locations = DriverTripRecord.objects.filter(ending_location__icontains=query).values_list('ending_location', flat=True).distinct()

    unique_locations = list(set(starting_locations) | set(ending_locations))
    return JsonResponse({'locations': unique_locations})


@login_required
def report(request, trip_id):
    trip = DriverTripRecord.objects.get(pk=trip_id)
    fuel_purchases = FuelPurchaseRecord.objects.all()  # Adjust query as needed
    client = OpenAICompletionClient('gpt-4o-mini')
    start_location = trip.starting_location
    ending_location = trip.ending_location
    start_mileage = trip.starting_mileage
    end_mileage = trip.ending_mileage

    journey_detail = trip.stops.all().values_list()

    response = client.send_request(data=journey_detail, start_location=start_location, ending_location=ending_location, start_mileage=start_mileage, end_mileage=end_mileage)

    return render(request, 'report.html', {'trip': trip, 'stops': response, 'fuel_purchases': fuel_purchases, })
