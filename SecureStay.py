from dataclasses import dataclass
from enum import Enum


class RoomType(Enum):
    FAMILY = "FR"
    BALCONY = "BR"
    SUITE = "SR"


@dataclass
class Room:
    id: str
    floor: int
    room_type: RoomType
    occupied: bool = False


@dataclass
class Guest:
    id: str
    verified: bool
    payment_success: bool
    requested_type: RoomType


class SecureStaySystem:
    def __init__(self, rooms):
        self.rooms = rooms

    def available_rooms(self):
        return [r for r in self.rooms if not r.occupied]

    def match_room(self, guest):
        for room in self.available_rooms():
            if room.room_type == guest.requested_type:
                return room
        return None

    def verify_identity(self, guest):
        return guest.verified

    def verify_payment(self, guest):
        return guest.payment_success

    def process_booking(self, guest):
        P = self.verify_identity(guest)
        if not P:
            return "DENIED: Identity verification failed"

        V = self.available_rooms()
        if not V:
            return "DENIED: No available rooms"

        room = self.match_room(guest)
        R = room is not None
        if not R:
            return "DENIED: No matching room type"

        T = self.verify_payment(guest)
        if not T:
            return "DENIED: Payment unsuccessful"

        room.occupied = True
        return f"APPROVED: Room {room.id} assigned on floor {room.floor}"


