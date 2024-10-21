import os
import json
from datetime import date, datetime
from ai_assistant.models import (
    RestaurantReservation,
    TripReservation,
    HotelReservation,
    TripType,
)
from ai_assistant.config import get_agent_settings

SETTINGS = get_agent_settings()

def custom_serializer(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()  
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def save_reservation(reservation):
    reservation_dict = reservation.model_dump() 
    reservation_dict["reservation_type"] = reservation.__class__.__name__

    reservations = []
    if os.path.exists(SETTINGS.log_file):
        with open(SETTINGS.log_file, "r") as file:
            try:
                reservations = json.load(file)
            except json.JSONDecodeError:
                print("Error: El archivo trip.json está corrupto o vacío, inicializando nuevo.")
                reservations = []

    reservations.append(reservation_dict)
    with open(SETTINGS.log_file, "w") as file:
        json.dump(reservations, file, indent=4, default=custom_serializer)

    print(f"Reserva guardada en {SETTINGS.log_file}: {reservation_dict}")