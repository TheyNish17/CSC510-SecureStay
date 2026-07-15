# booking.py
from typing import List, Optional
from data import HOTEL_ROOMS
from models import Room, RoomType, BookingRequest

def get_all_rooms() -> List[Room]:
    """Compiles the complete set R of Room objects from our data store."""
    all_rooms = []
    for floor_num, rooms in HOTEL_ROOMS.items():
        for r in rooms:
            all_rooms.append(Room(id=r["id"], type=r["type"], is_occupied=r["is_occupied"], floor=floor_num))
    return all_rooms

def find_available_room(req_type: RoomType) -> Optional[Room]:
    """
    Implements A = R - O
    Filters the total set of rooms (R) by type, removing occupied rooms (O).
    """
    R = get_all_rooms()
    # Filter by type and ensure it's not occupied (R - O)
    A = [room for room in R if room.type == req_type and not room.is_occupied]
    
    # Return the first available room if the set A is not empty
    return A[0] if A else None

def update_room_occupancy(room_id: int, status: bool):
    """Updates the database state to prevent double-booking."""
    for floor_num, rooms in HOTEL_ROOMS.items():
        for r in rooms:
            if r["id"] == room_id:
                r["is_occupied"] = status
                return