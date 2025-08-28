from django.shortcuts import render, redirect, get_object_or_404
from .models import TravelOption, Booking
from django.contrib.auth.decorators import login_required
from django.db import transaction

def travel_list(request):
    travel_options = TravelOption.objects.all()
    ttype = request.GET.get('type')
    source = request.GET.get('source')
    dest = request.GET.get('destination')
    date = request.GET.get('date')
    if ttype:
        travel_options = travel_options.filter(type=ttype)
    if source:
        travel_options = travel_options.filter(source__icontains=source)
    if dest:
        travel_options = travel_options.filter(destination__icontains=dest)
    if date:
        travel_options = travel_options.filter(departure_datetime__date=date)
    return render(request,'travel_list.html',{'travel_options':travel_options})

@login_required
def book_travel(request, travel_id):
    travel = get_object_or_404(TravelOption, travel_id=travel_id)
    if request.method=='POST':
        seats = int(request.POST.get('number_of_seats',1))
        if seats<=0 or seats>travel.available_seats:
            return render(request,'booking_form.html',{'travel':travel,'error':'Invalid number of seats'})
        with transaction.atomic():
            travel.available_seats -= seats
            travel.save(update_fields=['available_seats'])
            Booking.objects.create(user=request.user, travel_option=travel, number_of_seats=seats, total_price=seats*travel.price)
        return redirect('my_bookings')
    return render(request,'booking_form.html',{'travel':travel})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request,'my_bookings.html',{'bookings':bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.cancel()
    return redirect('my_bookings')
