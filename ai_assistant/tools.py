from random import randint
from datetime import date, datetime
from llama_index.core.tools import QueryEngineTool, FunctionTool, ToolMetadata
from ai_assistant.rags import TravelGuideRAG
from ai_assistant.prompts import travel_guide_qa_tpl, travel_guide_description
from ai_assistant.config import get_agent_settings
from ai_assistant.models import (
    TripReservation,
    TripType,
    HotelReservation,
    RestaurantReservation,
)
from ai_assistant.utils import save_reservation


SETTINGS = get_agent_settings()

travel_guide_tool = QueryEngineTool(
    query_engine=TravelGuideRAG(
        store_path=SETTINGS.travel_guide_store_path,
        data_dir=SETTINGS.travel_guide_data_path,
        qa_prompt_tpl=travel_guide_qa_tpl,
    ).get_query_engine(),
    metadata=ToolMetadata(
        name="travel_guide", 
        description=travel_guide_description, 
        return_direct=False
    ),
)


def reserve_flight(date_str: str, departure: str, destination: str) -> TripReservation:
   
    print(f"Reservando vuelo desde {departure} hacia {destination} para la fecha {date_str}.")
    reservation = TripReservation(
        trip_type=TripType.flight,
        departure=departure,
        destination=destination,
        date=date.fromisoformat(date_str),
        cost=randint(200, 700),
    )
    save_reservation(reservation)
    return reservation

flight_tool = FunctionTool(
    fn=reserve_flight, 
    metadata=ToolMetadata(
        name="flight_tool",
        description="Esta herramienta permite reservar vuelos nacionales e internacionales.",
        return_direct=False
    )
)


def reserve_bus(date_str: str, departure: str, destination: str) -> TripReservation:
    print(f"Reservando bus desde {departure} hacia {destination} para la fecha {date_str}.")
    reservation = TripReservation(
        trip_type=TripType.bus,
        departure=departure,
        destination=destination,
        date=date.fromisoformat(date_str),
        cost=randint(50, 300),
    )
    save_reservation(reservation)
    return reservation


bus_tool = FunctionTool(
    fn=reserve_bus, 
    metadata=ToolMetadata(
        name="bus_tool",
        description="Esta herramienta permite reservar tickets de bus para rutas nacionales.",
        return_direct=False
    )
)

def reserve_hotel(checkin_date: str, checkout_date: str, hotel_name: str, city: str) -> HotelReservation:
   
    print(f"Reservando hotel {hotel_name} en {city} desde {checkin_date} hasta {checkout_date}.")
    reservation = HotelReservation(
        checkin_date=date.fromisoformat(checkin_date),
        checkout_date=date.fromisoformat(checkout_date),
        hotel_name=hotel_name,
        city=city,
        cost=randint(500, 1500),
    )
    save_reservation(reservation)
    return reservation

hotel_tool = FunctionTool(
    fn=reserve_hotel, 
    metadata=ToolMetadata(
        name="hotel_tool",
        description="Esta herramienta permite reservar habitaciones de hotel en cualquier ciudad.",
        return_direct=False
    )
)


def reserve_restaurant(date_time: str, restaurant: str, city: str, dish: str = "not specified") -> RestaurantReservation:
    
    reservation_time = datetime.fromisoformat(date_time)
    print(f"Reservando restaurante {restaurant} en {city} para la fecha y hora {reservation_time}.")
    reservation = RestaurantReservation(
        reservation_time=reservation_time,
        restaurant=restaurant,
        city=city,
        dish=dish,
        cost=randint(20, 100),
    )
    save_reservation(reservation)
    return reservation

restaurant_tool = FunctionTool(
    fn=reserve_restaurant, 
    metadata=ToolMetadata(
        name="restaurant_tool",
        description="Esta herramienta permite reservar mesas en restaurantes de cualquier ciudad.",
        return_direct=False
    )
)
