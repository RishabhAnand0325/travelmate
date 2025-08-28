# TravelMate — Simple Travel Booking (Django + MySQL)

A minimal travel booking web app where users can browse travel options (flight/train/bus),
book seats, and manage their bookings.

## Features
- Django auth (signup/login/logout) + profile update
- Travel options with filters: type, source, destination, date
- Booking with seat validation and atomic inventory updates
- View current and past bookings; cancel to restore seats
- Responsive Bootstrap UI (Django templates)
- MySQL database
- Unit tests for critical flows

## Quickstart

1. **Clone / unzip** this project and `cd` into it.
2. Create and activate a virtual environment, then install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with your MySQL creds:
   ```ini
   DJANGO_SECRET_KEY=change-me
   DJANGO_DEBUG=1
   DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
   MYSQL_DATABASE=travelmate
   MYSQL_USER=root
   MYSQL_PASSWORD=yourpassword
   MYSQL_HOST=127.0.0.1
   MYSQL_PORT=3306
   ```
4. **Create database** in MySQL (if not already):
   ```sql
   CREATE DATABASE travelmate CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
5. **Migrate & run**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
6. Visit http://127.0.0.1:8000 to browse. Use the admin at `/admin` to add `TravelOption` entries.

## Running tests
```bash
python manage.py test
```

## Notes
- Inventory checks are validated in the form and enforced again inside a DB transaction using `select_for_update`.
- Cancelling a booking returns seats to availability.
- Timezone is set to `Asia/Kolkata` in settings.
