from django.contrib import admin
from .models import Airport, Airline, Aircraft, Flight, Gate




admin.site.register(Airport)
admin.site.register(Airline)
admin.site.register(Aircraft)
admin.site.register(Flight)
admin.site.register(Gate)
