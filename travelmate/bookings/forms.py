from django import forms
from .models import Booking
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['travel_option', 'number_of_seats']
