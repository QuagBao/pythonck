from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime

class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Movie(models.Model):
    STATUS_CHOICES = [
        ('coming_soon', 'Coming Soon'),
        ('now_showing', 'Now Showing'),
    ]

    id = models.AutoField(primary_key=True)  # Thêm trường id với auto increment
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.PositiveIntegerField()  # Duration in minutes
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    release_date = models.DateField(default=datetime.date.today)
    director = models.CharField(max_length=255, default='Unknown')
    cast = models.CharField(max_length=255, default='Unknown')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='coming_soon')
    image = models.ImageField(null=True, blank=True)
    country = models.CharField(max_length=255, default='Unknown')
    subtitle = models.CharField(max_length=255, default='Unknown')
    genres = models.ManyToManyField(Genre, related_name='movies')
    trailer = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title


class Cinema(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='cinemas', default=1)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    total_halls = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}, {self.city.name}"

class Hall(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name='halls')
    name = models.CharField(max_length=50)
    total_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.cinema.name})"
    
    def clean(self):
        if self.cinema.halls.count() >= self.cinema.total_halls:
            raise ValidationError(f"The cinema '{self.cinema.name}' already has the maximum number of halls ({self.cinema.total_halls}).")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='showtimes')
    show_date = models.DateField()
    start_time = models.TimeField()
    remaining_seats = models.PositiveIntegerField()  # Number of remaining seats in the hall

    def __str__(self):
        return f"{self.movie.title} at {self.hall.name} on {self.show_date} {self.start_time}"
    
    def clean(self):
        if self.movie.status != 'now_showing':
            raise ValidationError('Only movies that are now showing can have showtimes.')
    
    def save(self, *args, **kwargs):
        # Call the clean method to enforce the constraint
        self.clean()
        super().save(*args, **kwargs)

class Ticket(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='tickets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    seat_number = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket for {self.showtime.movie.title} at {self.showtime.hall.name} on {self.showtime.show_date} {self.showtime.start_time} - Seat {self.seat_number}"

