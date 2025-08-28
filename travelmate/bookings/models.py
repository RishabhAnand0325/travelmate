from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class TravelOption(models.Model):
    TRAVEL_TYPES=[('Flight','Flight'),('Train','Train'),('Bus','Bus')]
    travel_id=models.CharField(max_length=20, unique=True)
    type=models.CharField(max_length=10, choices=TRAVEL_TYPES)
    source=models.CharField(max_length=100)
    destination=models.CharField(max_length=100)
    departure_datetime=models.DateTimeField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    available_seats=models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.travel_id} - {self.type} {self.source}→{self.destination}"

class Booking(models.Model):
    STATUS_CHOICES=[('Confirmed','Confirmed'),('Cancelled','Cancelled')]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    travel_option=models.ForeignKey(TravelOption,on_delete=models.PROTECT, related_name='bookings')
    number_of_seats=models.PositiveIntegerField()
    total_price=models.DecimalField(max_digits=12,decimal_places=2)
    booking_date=models.DateTimeField(default=timezone.now)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='Confirmed')
    def cancel(self):
        if self.status!='Cancelled':
            self.status='Cancelled'
            self.travel_option.available_seats+=self.number_of_seats
            self.travel_option.save(update_fields=['available_seats'])
            self.save(update_fields=['status'])
