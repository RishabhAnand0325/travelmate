from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from .models import TravelOption, Booking
import datetime

class BookingFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='password', email='a@a.com')
        self.travel = TravelOption.objects.create(
            travel_id='FL123',
            type='Flight',
            source='Delhi',
            destination='Mumbai',
            departure_datetime=timezone.now() + datetime.timedelta(days=2),
            price=Decimal('4999.00'),
            available_seats=5
        )

    def test_user_can_register_and_login(self):
        resp = self.client.post(reverse('signup'), {
            'username':'bob','email':'b@b.com','first_name':'Bob','last_name':'B',
            'password1':'ASecurePass123','password2':'ASecurePass123'
        })
        self.assertEqual(resp.status_code, 302)  # redirect after signup
        # logout then login
        self.client.logout()
        login_ok = self.client.login(username='bob', password='ASecurePass123')
        self.assertTrue(login_ok)

    def test_booking_reduces_available_seats(self):
        self.client.login(username='alice', password='password')
        resp = self.client.post(reverse('create_booking', args=[self.travel.pk]), {'number_of_seats': 3})
        self.assertEqual(resp.status_code, 302)
        self.travel.refresh_from_db()
        self.assertEqual(self.travel.available_seats, 2)
        booking = Booking.objects.get(user=self.user)
        self.assertEqual(booking.total_price, Decimal('14997.00'))

    def test_cannot_overbook(self):
        self.client.login(username='alice', password='password')
        resp = self.client.post(reverse('create_booking', args=[self.travel.pk]), {'number_of_seats': 10})
        # Should not create booking and should show the detail page again
        self.assertEqual(resp.status_code, 200)
        self.travel.refresh_from_db()
        self.assertEqual(self.travel.available_seats, 5)
        self.assertEqual(Booking.objects.count(), 0)

    def test_cancel_restores_seats(self):
        self.client.login(username='alice', password='password')
        self.client.post(reverse('create_booking', args=[self.travel.pk]), {'number_of_seats': 2})
        booking = Booking.objects.get(user=self.user)
        self.client.get(reverse('cancel_booking', args=[booking.pk]))
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'Cancelled')
        self.travel.refresh_from_db()
        self.assertEqual(self.travel.available_seats, 5)
