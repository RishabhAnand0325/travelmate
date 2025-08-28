from django.urls import path
from . import views

urlpatterns=[
    path('', views.travel_list, name='travel_list'),
    path('book/<str:travel_id>/', views.book_travel, name='book_travel'),
    path('mybookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
