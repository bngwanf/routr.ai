# records/forms.py
from django.forms import inlineformset_factory

from .models import DriverTripRecord, FuelPurchaseRecord, Stop
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field


class DriverTripRecordForm(forms.ModelForm):
    class Meta:
        model = DriverTripRecord
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('date', css_class='form-group col-md-6 mb-0'),
                Column('company_name', css_class='form-group col-md-6 mb-0'),
                Column('address', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('driver_name', css_class='form-group col-md-6 mb-0'),
                Column('start_time', css_class='form-group col-md-3 mb-0'),
                Column('end_time', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('starting_mileage', css_class='form-group col-md-6 mb-0'),
                Column('ending_mileage', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('starting_location', css_class='form-group col-md-6 mb-0'),
                Column('ending_location', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),

        )


class FuelPurchaseRecordForm(forms.ModelForm):
    class Meta:
        model = FuelPurchaseRecord
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('trip_record', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('state', css_class='form-group col-md-6 mb-0'),
                Column('date', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('invoice_number', css_class='form-group col-md-6 mb-0'),
                Column('gallons', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('dollar_amount', css_class='form-group col-md-6 mb-0'),
                Column('fuel_stop_name', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Save')
        )

    def clean(self):
        cleaned_data = super().clean()
        gallons = cleaned_data.get('gallons')
        dollar_amount = cleaned_data.get('dollar_amount')

        if gallons is not None and gallons < 0:
            self.add_error('gallons', 'Gallons must be a positive number.')

        if dollar_amount is not None and dollar_amount < 0:
            self.add_error('dollar_amount', 'Dollar amount must be a positive number.')

        return cleaned_data

class StopForm(forms.ModelForm):
    class Meta:
        model = Stop
        fields = '__all__'
        widgets = {
            'customer_name': forms.TextInput(attrs={'size': '40', 'class': 'form-control'}),
            'customer_address': forms.TextInput(attrs={'size': '60', 'class': 'form-control'}),
            'pallets_in': forms.NumberInput(attrs={'size': '5', 'class': 'form-control'}),
            'pallets_out': forms.NumberInput(attrs={'size': '5', 'class': 'form-control'}),
            'comments': forms.TextInput(attrs={'size': '100', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = ''


StopFormSet = inlineformset_factory(DriverTripRecord, Stop, form=StopForm, extra=1, can_delete=True)
