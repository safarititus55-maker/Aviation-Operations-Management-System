# Aviation Operations Management System (AOMS)

## Overview

The Aviation Operations Management System (AOMS) is a Django-based software platform designed to support the management of aviation operations, including flight scheduling, airport resources, and future passenger service operations.

The goal of AOMS is to provide a centralized system that improves coordination, visibility, and efficiency in airport operations.

---

## Current Development Status

### Completed Modules

✅ Django project foundation  
✅ Airport management foundation  
✅ Airline management foundation  
✅ Aircraft management foundation  
✅ Flight management system  
✅ Gate management system  
✅ Database integration using Django ORM  
✅ GitHub version control setup  

---

## Technology Stack

- Python
- Django Framework
- SQLite Database (Development)
- HTML/CSS/JavaScript (Frontend - upcoming)
- Git & GitHub

---

## Current System Structure

---

## Upcoming Development Modules

The following modules will be developed progressively:

### Passenger Management
- Passenger profiles
- Passenger records
- Travel information

### Booking and Reservation System
- Flight reservations
- Ticket management
- Booking status tracking

### Check-in System
- Passenger check-in
- Seat allocation
- Boarding pass generation

### Airport Operations Dashboard
- Flight monitoring
- Gate allocation
- Operational reports

### Future Enhancements

- User authentication and roles
- Real-time notifications
- Analytics and reporting
- Cloud deployment

---

## Project Vision

To develop a complete aviation operations platform capable of supporting airport activities through automation, centralized information management, and improved operational decision-making.

---

## Developer

Safari Titus

Computing and Information Technology Graduate

---

## Version History

### Version 0.1 - Foundation

- Initial Django setup
- Core aviation models created
- Flight and Gate management foundation
- GitHub repository established

# Aviation Operations Management System (AOMS)

## Overview

The Aviation Operations Management System (AOMS) is a web-based application built using Django. It is designed to automate and manage airport and airline operations, including flight scheduling, passenger management, crew management, boarding, baggage handling, and airport operational workflows.

The project is being developed incrementally following software engineering best practices with Git version control and documentation updates at each milestone.

---

## Technologies

- Python 3
- Django 6
- SQLite (Development Database)
- HTML, CSS
- Django Admin
- Git & GitHub

---

## Completed Modules

### Core Aviation

- Airport
- Airline
- Aircraft
- Flight
- Gate

### Passenger Operations

- Passenger
- Booking
- Check-In
- Baggage
- Boarding

### Crew Operations

- Crew Member
- Crew Assignment

---

## Current Passenger Workflow

Airport
↓
Flight
↓
Passenger
↓
Booking
↓
Check-In
├── Baggage
└── Boarding
↓
Flight Departure

---

## Current Crew Workflow

Crew Member
↓
Crew Assignment
↓
Flight

---

## Database Relationships

- Airport → Flights
- Airport → Gates
- Airline → Aircraft
- Aircraft → Flights
- Flight → Bookings
- Flight → Crew Assignments
- Passenger → Bookings
- Booking → Check-In
- Check-In → Baggage
- Check-In → Boarding

---

## Current Features

- Airport Management
- Airline Management
- Aircraft Management
- Flight Management
- Gate Management
- Passenger Registration
- Flight Booking
- Passenger Check-In
- Baggage Tracking
- Boarding Management
- Crew Registration
- Crew Assignment
- Django Admin Management

---

## Development Roadmap

### ✅ Phase 1
- Airport
- Airline
- Aircraft
- Flight
- Gate

### ✅ Phase 2
- Passenger
- Booking
- Check-In
- Baggage
- Boarding

### ✅ Phase 3
- Crew Member
- Crew Assignment

### 🔄 Phase 4 (Next)
- Runway Management
- Flight Scheduling
- Arrival Management
- Departure Management
- Boarding Passes

### Future Phases
- Aircraft Maintenance
- Fuel Management
- Ticketing & Payments
- Notifications
- Reporting & Analytics
- REST API
- Authentication & Permissions

---

## Project Status

Current Milestone: **Passenger Operations and Crew Management Completed**

The project is under active development, with new aviation modules being added incrementally following professional software engineering practices.
