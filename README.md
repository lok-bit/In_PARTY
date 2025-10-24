# In PARTY – Event Management Platform

## Project Overview

In PARTY is a location-based event management platform that blends social features with gamification. Users can explore nearby events, create their own, and level up their in-app character by participating.

## Key Features

### 🗺️ Location Services

* Automatically detects the user’s location and shows events within a 5 km radius
* Visualizes event locations on a map
* Supports address search and geolocation

### 🎉 Event Management

* **Create Events:** publish event info, upload images, set time and venue
* **Join Events:** register, cancel registration, on-site check-in
* **Event Info:** view details and participant counts

### 🎮 Gamification

* Character creation and progression
* Level and experience system
* Partner/companion system
* Earn EXP by attending events

### 👤 User System

* Secure sign-up/sign-in (bcrypt password hashing)
* Session management
* Permission/role control

## Tech Stack

### Backend

* **Framework:** Flask (Python)
* **Database:** MySQL/MariaDB
* **Session Management:** Flask-Session
* **Password Hashing:** bcrypt
* **Geocoding:** Geopy (Nominatim, ArcGIS)

### Frontend

* HTML/CSS/JavaScript

## How to Use

### For General Users

1. **Register:** first-time users sign up; a character is created automatically
2. **Browse Events:** view nearby events on the home page map
3. **Join:** open an event to see details and register

