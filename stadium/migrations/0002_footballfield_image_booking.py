# Generated by Django 4.2.20 on 2025-03-09 03:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stadium', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FootballField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=100)),
                ('hourly_rate', models.DecimalField(decimal_places=2, max_digits=6)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fields', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('path', models.ImageField(blank=True, null=True, upload_to='media/images')),
                ('football_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stadium.footballfield')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='stadium.footballfield')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
