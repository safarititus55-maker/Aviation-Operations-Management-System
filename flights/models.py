from django.db import models
import uuid


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
class Passenger(models.Model):
    GENDER_CHOICES = [
        ("MALE", "Male"),
        ("FEMALE", "Female"),
        ("OTHER", "Other")
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    
    date_of_birth = models.DateField()
 
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )
    nationality = models.CharField(max_length=50)
    
    passpprt_number = models.CharField(
       max_length=50,
       unique=True
    )

    email = models.CharField(
        unique=True
    )

    phone_number = models.CharField(
        max_length=20
    )

    emergency_contact = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Booking(models.Model):
    CLASS_CHOICES = [
        ("ECONOMY", "Economy"),
        ("BUSINESS", "Business"),
        ("FIRST", "First Claass"),
    ]
  

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
        ("CHECKED_IN", "Checked in"),
    ]

    PAYMENT_CHOICES = [
        ("UNPAID", "Unpaid"),
        ("PAID", "Paid"),
        ("REFUNDED", "Refunded")
    ]

    booking_reference = models.CharField(
        max_length=12,
        unique=True,
        editable=False
    )

    passenger = models.ForeignKey(
        Passenger,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    seat_number = models.CharField(max_length=5)

    travel_class = models.CharField(
        max_length=20,
        choices=CLASS_CHOICES,
        default="ECONOMY"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="UNPAID"
    )

    booking_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            self.booking_reference = str(uuid.uuid4()).replace("-", "").upper()[:12]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_reference} - {self.passenger}"

from django.utils import timezone

class CheckIn(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CHECKED_IN", "Checked in"),
        ("BOARDED", "Boarded"),
        ("MISSED", "Missed Flifght"),
    ]

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="checkin"
    )

    seat_number = models.CharField(
        max_length=5,
        blank=True,
        null=True
    )

    baggage_count = models.PositiveIntegerField(default=0)

    baggage_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    boarding_pass_number = models.CharField(
        max_length=30,
        unique=True
    )

    status = models.CharField(
        max_length=200,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    def __str__(self):
        return f"{self.booking.booking_reference} - {self.status}"

class Baggage(models.Model):
    BAG_TYPE_CHOICES = [
        ("CHECKED", "Checked"),
        ("CARRY_ON", "Carry-On"),
        ("OVERSIZED", "Oversized"),
    ]

    STATUS_CHOICES = [
        ("CHECKED", "Checked"),
        ("LOADED", "Loaded"),
        ("IN_TRANSIT", "In Transit"),
        ("ARRIVED", "Arrived"),
        ("CLAIMED", "Claimed"),
        ("LOST", "Lost"),
    ]

    check_in = models.ForeignKey(
        CheckIn,
        on_delete=models.CASCADE,
        related_name="baggage"
    ) 

    bag_tag_number = models.CharField(
         max_length=30,
         unique=True
    )

    bag_type = models.CharField(
        max_length=20,
        choices=BAG_TYPE_CHOICES,
        default="CHECKED"
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    destination = models.ForeignKey(
        Airport,
        on_delete=models.PROTECT,
        related_name="arriving_baggage"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="CHECKED"
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.bag_tag_number} ({self.status})"

class Boarding(models.Model):
    STATUS_CHOICES = [
        ("WAITING", "Waiting"),
        ("BOARDED", "Boarded"),
        ("NO_SHOW", "No Show"),
        ("DENIED", "Denied Boarding"),
    ]

    check_in = models.OneToOneField(
        CheckIn,
        on_delete=models.CASCADE,
        related_name="boarding"
    )

    gate = models.ForeignKey(
        Gate,
        on_delete=models.PROTECT,
        related_name="boardings"
    )

    boarding_time = models.DateTimeField(default=timezone.now)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="WAITING"
    )

    boarded_by = models.CharField(
        max_length=100,
        blank=True,
    )

    remarks =  models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.check_in.booking.booking_reference} - {self.status}"

class CrewMember(models.Model):
    ROLE_CHOICES = [
        ("PILOT", "Pilot"),
        ("COPILOT", "Co-Pilot"),
        ("CABIN_CREW", "Cabin Crew"),
    ]

    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)

    employee_number = models.CharField(
        max_length=20,
        unique=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"

class CrewAssignment(models.Model):
    crew_member = models.ForeignKey(
        CrewMember,
        on_delete=models.CASCADE,
        related_name="assignments"
    )

    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="crew_assignment"
    )

    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("crew_member", "flight")
        ordering = ["flight"]

    def __str__(self):
        return f"{self.crew_member} --> {self.flight.flight_number}"


class Runway(models.Model):
    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("OCCUPIED", "Occupied"),
        ("MAINTENANCE", "Under Maintenance"),
        ("CLOSED", "Closed"),
    ]

    airport = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="runways"
    )

    runway_code = models.CharField(
        max_length=10,
        unique=True
    )

    length_meters = models.PositiveIntegerField()

    width_meters = models.PositiveIntegerField()

    surface_type = models.CharField(
        max_length=30,
        default="Asphalt"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="AVAILABLE"
    )

    lighting_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.airport.icao_code} - {self.runway_code}"
