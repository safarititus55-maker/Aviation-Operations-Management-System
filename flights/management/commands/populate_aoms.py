from django.core.management.base import BaseCommand
from django.utils import timezone
from flights.models import (
    Airport,
    Airline,
    Aircraft,
    Gate,
    Runway,
    Flight,
    Passenger,
    Booking,
    CrewMember,
    CrewAssignment,
)
from datetime import timedelta
import random


class Command(BaseCommand):
    help = "Populate AOMS with bulk test data"

    def handle(self, *args, **kwargs):

        self.stdout.write(
            self.style.WARNING("Starting AOMS database population...")
        )

        # ---------------------------------------------------------
        # 1. AIRPORTS
        # ---------------------------------------------------------

        airports_data = [
            ("HKJK", "NBO", "Jomo Kenyatta International Airport",
             "Nairobi", "Kenya", "Africa/Nairobi"),

            ("HKMO", "MBA", "Moi International Airport",
             "Mombasa", "Kenya", "Africa/Nairobi"),

            ("HKKI", "KIS", "Kisumu International Airport",
             "Kisumu", "Kenya", "Africa/Nairobi"),

            ("HKEL", "EDL", "Eldoret International Airport",
             "Eldoret", "Kenya", "Africa/Nairobi"),

            ("HUEN", "EBB", "Entebbe International Airport",
             "Entebbe", "Uganda", "Africa/Kampala"),

            ("HTDA", "DAR", "Julius Nyerere International Airport",
             "Dar es Salaam", "Tanzania", "Africa/Dar_es_Salaam"),

            ("HTZA", "ZNZ", "Abeid Amani Karume International Airport",
             "Zanzibar", "Tanzania", "Africa/Dar_es_Salaam"),

            ("HTKJ", "JRO", "Kilimanjaro International Airport",
             "Kilimanjaro", "Tanzania", "Africa/Dar_es_Salaam"),

            ("HRYR", "KGL", "Kigali International Airport",
             "Kigali", "Rwanda", "Africa/Kigali"),

            ("HAAB", "ADD", "Bole International Airport",
             "Addis Ababa", "Ethiopia", "Africa/Addis_Ababa"),

            ("HBBA", "BJM", "Bujumbura International Airport",
             "Bujumbura", "Burundi", "Africa/Bujumbura"),

            ("DGAA", "ACC", "Kotoka International Airport",
             "Accra", "Ghana", "Africa/Accra"),

            ("DNMM", "LOS", "Murtala Muhammed International Airport",
             "Lagos", "Nigeria", "Africa/Lagos"),

            ("FAOR", "JNB", "OR Tambo International Airport",
             "Johannesburg", "South Africa", "Africa/Johannesburg"),

            ("FACT", "CPT", "Cape Town International Airport",
             "Cape Town", "South Africa", "Africa/Cape_Town"),

            ("HECA", "CAI", "Cairo International Airport",
             "Cairo", "Egypt", "Africa/Cairo"),

            ("OMDB", "DXB", "Dubai International Airport",
             "Dubai", "United Arab Emirates", "Asia/Dubai"),

            ("OTHH", "DOH", "Hamad International Airport",
             "Doha", "Qatar", "Asia/Qatar"),

            ("EGLL", "LHR", "Heathrow Airport",
             "London", "United Kingdom", "Europe/London"),

            ("LFPG", "CDG", "Charles de Gaulle Airport",
             "Paris", "France", "Europe/Paris"),
        ]

        airports = {}

        for data in airports_data:
            icao_code, iata_code, name, city, country, tz = data

            # Try to find the airport using ICAO code first
            airport = Airport.objects.filter(
                icao_code=icao_code
            ).first()

            # If ICAO is not found, try IATA code
            if airport is None:
                airport = Airport.objects.filter(
                    iata_code=iata_code
                ).first()

            # Create a new airport if it does not exist
            if airport is None:
                airport = Airport.objects.create(
                    icao_code=icao_code,
                    iata_code=iata_code,
                    name=name,
                    city=city,
                    country=country,
                    timezone=timezone,
                )

            else:
                # Update existing airport information
                airport.icao_code = icao_code
                airport.iata_code = iata_code
                airport.name = name
                airport.city = city
                airport.country = country
                airport.timezone = tz
                airport.save()

            # Store airport using its IATA code
            airports[iata_code] = airport

        self.stdout.write(
            self.style.SUCCESS(
                f"Airports ready: {len(airports)}"
            )
        )


        self.stdout.write(
            self.style.SUCCESS(
                f"Airports ready: {len(airports)}"
            )
        )

        # ---------------------------------------------------------
        # 2. AIRLINES
        # ---------------------------------------------------------

        
        airlines_data = [
            ("KQA", "KQ", "Kenya Airways"),
            ("JMA", "JM", "Jambojet"),
            ("ETH", "ET", "Ethiopian Airlines"),
            ("UGD", "UR", "Uganda Airlines"),
            ("RWD", "WB", "RwandAir"),
            ("ATC", "TC", "Air Tanzania"),
            ("PRF", "PW", "Precision Air"),
            ("MSR", "MS", "EgyptAir"),
            ("SAA", "SA", "South African Airways"),
            ("MAU", "MK", "Air Mauritius"),
            ("BAW", "BA", "British Airways"),
            ("KLM", "KL", "KLM"),
            ("AFR", "AF", "Air France"),
            ("DLH", "LH", "Lufthansa"),
            ("THY", "TK", "Turkish Airlines"),
            ("UAE", "EK", "Emirates"),
            ("QTR", "QR", "Qatar Airways"),
        ]

        airlines = {}

        for icao, iata, name in airlines_data:
            airline, created = Airline.objects.get_or_create(
                icao_code=icao,
                defaults={
                    "iata_code": iata,
                    "name": name,
                },
            )

            airlines[iata] = airline

        self.stdout.write(
            self.style.SUCCESS(
                f"Airlines ready: {len(airlines)}"
            )
        )

        # ---------------------------------------------------------
        # 3. AIRCRAFT
        # ---------------------------------------------------------

        aircraft_types = [
            ("Boeing", "737-800", 162),
            ("Boeing", "787-9", 296),
            ("Airbus", "A320-200", 180),
            ("Airbus", "A321neo", 220),
            ("Embraer", "E190", 100),
        ]

        aircraft_list = []

        for i in range(30):

            airline_code = random.choice(list(airlines.keys()))
            airline = airlines[airline_code]

            manufacturer, model, capacity = random.choice(
                aircraft_types
            )

            registration = f"5Y-{100 + i:03d}"

            aircraft, created = Aircraft.objects.get_or_create(
                registration=registration,
                defaults={
                    "manufacturer": manufacturer,
                    "model": model,
                    "capacity": capacity,
                    "airline": airline,
                    "status": "AVAILABLE",
                },
            )

            aircraft_list.append(aircraft)

        self.stdout.write(
            self.style.SUCCESS(
                f"Aircraft ready: {len(aircraft_list)}"
            )
        )

        # ---------------------------------------------------------
        # 4. GATES
        # ---------------------------------------------------------

        gates = []

        for i, (iata_code, airport) in enumerate(
            airports.items()
        ):

            for gate_number in range(1, 3):

                gate, created = Gate.objects.get_or_create(
                    airport=airport,
                    gate_number=f"G{gate_number}",
                    defaults={
                        "terminal": "T1",
                        "status": "AVAILABLE",
                    },
                )

                gates.append(gate)

        self.stdout.write(
            self.style.SUCCESS(
                f"Gates ready: {len(gates)}"
            )
        )

        # ---------------------------------------------------------
        # 5. RUNWAYS
        # ---------------------------------------------------------

        runways = []

        for i, airport in enumerate(airports.values()):

            runway_code = f"{airport.iata_code}-RWY"

            runway, created = Runway.objects.get_or_create(
                runway_code=runway_code,
                defaults={
                    "airport": airport,
                    "length_meters": random.choice(
                        [2500, 2800, 3000, 3500, 4000]
                    ),
                    "width_meters": random.choice(
                        [45, 50, 60]
                    ),
                    "surface_type": "Asphalt",
                    "status": "AVAILABLE",
                    "lighting_available": True,
                },
            )

            runways.append(runway)

        self.stdout.write(
            self.style.SUCCESS(
                f"Runways ready: {len(runways)}"
            )
        )

        # ---------------------------------------------------------
        # 6. FLIGHTS
        # ---------------------------------------------------------

        flight_routes = [
            ("KQ", "NBO", "LHR"),
            ("KQ", "NBO", "EBB"),
            ("KQ", "NBO", "ADD"),
            ("KQ", "NBO", "JNB"),
            ("KQ", "NBO", "DAR"),
            ("KQ", "NBO", "ZNZ"),
            ("KQ", "NBO", "JRO"),
            ("ET", "ADD", "NBO"),
            ("ET", "ADD", "LHR"),
            ("ET", "ADD", "DXB"),
            ("WB", "KGL", "NBO"),
            ("WB", "KGL", "LHR"),
            ("TC", "DAR", "NBO"),
            ("TC", "DAR", "DXB"),
            ("BA", "LHR", "NBO"),
            ("BA", "LHR", "CDG"),
            ("EK", "DXB", "NBO"),
            ("EK", "DXB", "LHR"),
            ("QR", "DOH", "NBO"),
            ("QR", "DOH", "LHR"),
            ("AF", "CDG", "NBO"),
            ("LH", "LHR", "NBO"),
        ]

        flights = []

        base_time = timezone.now() + timedelta(days=1)

        for i, route in enumerate(flight_routes):

            airline_code, departure, arrival = route

            airline = airlines[airline_code]
            departure_airport = airports[departure]
            arrival_airport = airports[arrival]

            aircraft = random.choice(aircraft_list)
            gate = random.choice(gates)

            flight_number = f"{airline_code}{100 + i}"

            departure_time = base_time + timedelta(
                hours=i * 2
            )

            arrival_time = departure_time + timedelta(
                hours=random.randint(1, 8)
            )

            flight, created = Flight.objects.get_or_create(
                flight_number=flight_number,
                defaults={
                    "airline": airline,
                    "aircraft": aircraft,
                    "departure_airport": departure_airport,
                    "arrival_airport": arrival_airport,
                    "scheduled_departure": departure_time,
                    "scheduled_arrival": arrival_time,
                    "gate": gate,
                    "status": "SCHEDULED",
                },
            )

            flights.append(flight)

        self.stdout.write(
            self.style.SUCCESS(
                f"Flights ready: {len(flights)}"
            )
        )

        # ---------------------------------------------------------
        # 7. PASSENGERS
        # ---------------------------------------------------------

        first_names = [
            "John", "Peter", "James", "David", "Michael",
            "Daniel", "Samuel", "Brian", "Joseph", "Kevin",
            "Mary", "Jane", "Grace", "Sarah", "Ann",
            "Faith", "Lucy", "Esther", "Linda", "Susan",
        ]

        last_names = [
            "Kamau", "Otieno", "Mwangi", "Ochieng",
            "Kiptoo", "Mutua", "Wanjiku", "Njoroge",
            "Kariuki", "Maina", "Kiprotich", "Okello",
        ]

        passengers = []

        for i in range(100):

            first_name = random.choice(first_names)
            last_name = random.choice(last_names)

            passenger, created = Passenger.objects.get_or_create(
                passpprt_number=f"P{100000 + i}",
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "date_of_birth": timezone.now().date()
                    - timedelta(days=random.randint(18 * 365, 65 * 365)),
                    "gender": random.choice(
                        ["MALE", "FEMALE"]
                    ),
                    "nationality": "Kenyan",
                    "email": f"passenger{i}@example.com",
                    "phone_number": f"+254700{100000 + i}",
                    "emergency_contact": "Emergency Contact",
                },
            )

            passengers.append(passenger)

        self.stdout.write(
            self.style.SUCCESS(
                f"Passengers ready: {len(passengers)}"
            )
        )

        # ---------------------------------------------------------
        # 8. BOOKINGS
        # ---------------------------------------------------------

        bookings = []

        for i in range(150):

            passenger = random.choice(passengers)
            flight = random.choice(flights)

            booking, created = Booking.objects.get_or_create(
                passenger=passenger,
                flight=flight,
                seat_number=f"{random.randint(1, 40)}{random.choice(['A', 'B', 'C', 'D', 'E', 'F'])}",
                defaults={
                    "travel_class": random.choice(
                        ["ECONOMY", "BUSINESS", "FIRST"]
                    ),
                                        "payment_status": random.choice(
                        ["PAID", "PAID", "UNPAID"]
                    ),
                },
            )

            bookings.append(booking)

        self.stdout.write(
            self.style.SUCCESS(
                f"Bookings ready: {len(bookings)}"
            )
        )

        # ---------------------------------------------------------
        # COMPLETE
        # ---------------------------------------------------------

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "========================================"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                " AOMS DATABASE POPULATION COMPLETED"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "========================================"
            )
        )

        self.stdout.write(
            f"Airports:   {Airport.objects.count()}"
        )

        self.stdout.write(
            f"Airlines:   {Airline.objects.count()}"
        )

        self.stdout.write(
            f"Aircraft:   {Aircraft.objects.count()}"
        )

        self.stdout.write(
            f"Gates:      {Gate.objects.count()}"
        )

        self.stdout.write(
            f"Runways:    {Runway.objects.count()}"
        )

        self.stdout.write(
            f"Flights:    {Flight.objects.count()}"
        )

        self.stdout.write(
            f"Passengers: {Passenger.objects.count()}"
        )

        self.stdout.write(
            f"Bookings:   {Booking.objects.count()}"
        )

