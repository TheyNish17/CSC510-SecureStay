# models.py
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

# RoomType Enums: BR, SR, FR
class RoomType(str, Enum):
    FAMILY = "Family"
    BALCONY = "Balcony"
    SUITE = "Suite"

# R: Room object
class Room(BaseModel):
    id: int
    type: RoomType
    is_occupied: bool
    floor: int # Loc: R -> F mapping

# Request shape from the frontend
class BookingRequest(BaseModel):
    guest_name: str
    has_id: bool          # P: Identity verified
    payment_verified: bool # V: Payment cleared
    room_type: RoomType   # ReqType