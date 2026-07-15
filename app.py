# app.py

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models import BookingRequest, RoomType
from booking import find_available_room, update_room_occupancy, get_all_rooms
from logic import verify_booking_logic

app = FastAPI(title="SecureStay Reception")

# Setup templates and static files locations
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# app.py

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Renders the Receptionist Dashboard showing live room statuses."""
    # We create a clean context variables dictionary explicitly 
    context = {
        "request": request, 
        "rooms": get_all_rooms(),
        "room_types": [e.value for e in RoomType]
    }
    
    return templates.TemplateResponse(request=request, name="index.html", context=context)

@app.post("/book")
async def process_booking(
    guest_name: str = Form(...),
    room_type: RoomType = Form(...),
    has_id: bool = Form(False),
    payment_verified: bool = Form(False)
):
    """Processes the reception submission and evaluates math/logic constraints."""
    # 1. Instantiate the request frame
    req = BookingRequest(
        guest_name=guest_name,
        room_type=room_type,
        has_id=has_id,
        payment_verified=payment_verified
    )
    
    # 2. Compute available rooms (A = R - O)
    target_room = find_available_room(req.room_type)
    
    # 3. Evaluate safety logic (Z = P ∧ V ∧ R ∧ T)
    booking_approved = verify_booking_logic(req, target_room)
    
    if booking_approved and target_room:
        # Commit Book: G -> R mapping by locking the room
        update_room_occupancy(target_room.id, status=True)
        return {
            "status": "APPROVED",
            "message": f"Booking successful for {guest_name}!",
            "room_id": target_room.id,
            "floor": target_room.floor
        }
    else:
        # Diagnosing the logical failure
        reason = "Unknown error"
        if not has_id: reason = "Guest Identity Unverified (P failed)"
        elif not payment_verified: reason = "Payment Processing Failed (V failed)"
        elif not target_room: reason = f"No vacant rooms available for type: {room_type.value} (A empty)"
        
        return {
            "status": "DENIED",
            "message": f"Booking Denied: {reason}"
        }
