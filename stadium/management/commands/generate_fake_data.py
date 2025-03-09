# your_app/management/commands/generate_sample_data.py

import random
from datetime import date, timedelta, time
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from stadium.models import FootballField, Booking, User
from faker import Faker

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Generate sample data for FootballField and Booking'

    def add_arguments(self, parser):
        parser.add_argument(
            '--num_fields',
            type=int,
            default=100,
            help='Number of FootballField objects to create (default: 1000)'
        )
        parser.add_argument(
            '--num_bookings',
            type=int,
            default=100,
            help='Number of Booking objects to create (default: 1000)'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        num_fields = options['num_fields']
        num_bookings = options['num_bookings']

        self.stdout.write(f"Generating {num_fields} FootballField records...")
        fields = []
        for _ in range(num_fields):
            user = User.objects.get(id=1)
            lat = random.uniform(-90, 90)
            lon = random.uniform(-180, 180)
            field = FootballField(
                owner=user,  # You can assign a random user if needed.
                name=fake.company(),
                address=fake.address(),
                contact=fake.phone_number(),
                hourly_rate=round(random.uniform(10, 100), 2),
                latitude=lat,
                longitude=lon
            )
            fields.append(field)
        FootballField.objects.bulk_create(fields)
        self.stdout.write("FootballField records created.")

        # Retrieve the created fields for use in bookings.
        fields = list(FootballField.objects.all())

        # Ensure there are users available for booking (you might need to create one manually or use a fixture)
        users = list(User.objects.all())
        if not users:
            self.stdout.write("No users found. Please create some users first.")
            return

        self.stdout.write(f"Generating {num_bookings} Booking records...")
        bookings = []
        for _ in range(num_bookings):
            print(_)
            field = random.choice(fields)
            # Generate a random date within the next 30 days.
            b_date = date.today() + timedelta(days=random.randint(0, 30))
            start_hour = random.randint(6, 20)
            start = time(hour=start_hour, minute=0)
            end = time(hour=start_hour + 1, minute=0)
            booking = Booking(
                user=random.choice(users),
                field=field,
                booking_date=b_date,
                start_time=start,
                end_time=end,
            )
            bookings.append(booking)
        Booking.objects.bulk_create(bookings)
        self.stdout.write("Booking records created.")
