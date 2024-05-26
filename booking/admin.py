from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(City)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Cinema)
admin.site.register(Hall)
admin.site.register(Showtime)
admin.site.register(Ticket)

