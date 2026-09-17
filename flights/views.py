from django.shortcuts import render
from .models import (
    Airport,
    Airline,
    Aircraft,
    Flight,
    Gate,
    Passenger,
    Booking,
    CheckIn,
    Baggage,
    Boarding,
    CrewMember,
    Runway,
)


def dashboard(request):
    context = {
        "airport_count": Airport.objects.count(),
        "airline_count": Airline.objects.count(),
        "aircraft_count": Aircraft.objects.count(),
        "flight_count": Flight.objects.count(),
        "gate_count": Gate.objects.count(),
        "passenger_count": Passenger.objects.count(),
        "booking_count": Booking.objects.count(),
        "checkin_count": CheckIn.objects.count(),
        "baggage_count": Baggage.objects.count(),
        "boarding_count": Boarding.objects.count(),
        "crew_count": CrewMember.objects.count(),
        "runway_count": Runway.objects.count(),
        "flights": Flight.objects.select_related(
            "airline",
            "aircraft",
            "departure_airport",
            "arrival_airport",
            "gate",
        ).order_by("scheduled_departure")[:10],
    }

    return render(request, "flights/dashboard.html", context)
