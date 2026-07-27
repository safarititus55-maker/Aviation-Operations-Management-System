from django.db import models


class Airport(models.Model):
    icao_code = models.CharField(max_length=4, unique=True)
    iata_code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    timezone = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.icao_code} - {self.name}"

class Airline(models.Model):
    icao_code = models.CharField(max_length=3, unique=True)
    iata_code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
       return f"{self.icao_code} - {self.name}"

class Aircraft(models.Model):
    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("IN_FLIGHT", "In flight"),
        ("MAINTENANCE", "Maintenance"),
    ]

    registration = models.CharField(max_length=10, unique=True)
    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()

    airline = models.ForeignKey(
        Airline,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="AVAILABLE"
    )

    def __str__(self):
        return f"{self.registration} - {self.manufacturer} {self.model}"

class Flight(models.Model):
    STATUS_CHOICES = [
        ("SCHEDULED", "Scheduled"),
        ("BOARDING", "Boarding"),
        ("DEPARTED", "Departed"),
        ("ARRIVED", "Arrived"),
        ("DELAYED", "Delayed"),
        ("CANCELLED", "Canceled"),
        ("DIVERTED", "Diverted"),
    ]
    flight_number = models.CharField(max_length=10, unique=True)
    airline = models.ForeignKey(
        Airline,
        on_delete=models.CASCADE
    )
    aircraft = models.ForeignKey(
        Aircraft,
        on_delete=models.CASCADE
    )
    departure_airport = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="departing_flights"
    )
    arrival_airport = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="arriving_flights"
    )
    scheduled_departure = models.DateTimeField()
    scheduled_arrival = models.DateTimeField()
    actual_departure = models.DateTimeField(
        null=True,
        blank=True
    )
    actual_arrival = models.DateTimeField(
        null=True,
        blank=True
    )
    gate = models.ForeignKey(
        "Gate",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="SCHEDULED"
    )
    def __str__(self):
        return f"{self.flight_number} ({self.departure_airport} -{self.arrival_airport})"

class Gate(models.Model):
    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("OCCUPIED", "Occupied"),
        ("MAINTENANCE", "Maintenance"),
        ("CLOSED", "Closed"),
    ]
    gate_number = models.CharField(max_length=10)
    terminal = models.CharField(max_length=20)
    airport = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="gates"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="AVAILABLE"
    )
    def __str__(self):
        return f"{self.airport.icao_code} - Terminal {self.terminal} Gate {self.gate_number}"
           
  
