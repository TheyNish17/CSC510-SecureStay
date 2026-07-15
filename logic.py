# logic.py
from models import BookingRequest, Room

def verify_booking_logic(request: BookingRequest, available_room: Optional[Room]) -> bool:
    """
    Evaluates Propositional Logic for a valid booking.
    P: Guest has verified ID
    V: Payment is verified
    R: A room of the requested type is available
    T: Room is not currently occupied (Double-booking check)
    Z: Booking Approved
    
    Formula: Z = P ∧ V ∧ R ∧ T
    """
    P = request.has_id
    V = request.payment_verified
    R = available_room is not None
    T = available_room.is_occupied is False if available_room else False
    
    # Propositional evaluation
    Z = P and V and R and T
    return Z