# app.py
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# 1. REMOVED THE OLD SYNCHRONIZATION IMPORTS HERE
from models import BookingRequest, RoomType
from logic import verify_booking_logic

# 2. IMPORT BOTH THE READ AND WRITE UTILITIES FROM YOUR INVENTORY CORNERSTONE
from inventory import calculate_metrics, reserve_room

app = FastAPI(title="SecureStay Reception")

# Setup templates and static files locations
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/reset-inventory")
async def reset_inventory():
    """Deletes the current JSON database file to wipe all bookings."""
    DB_FILE = "room_inventory.json"
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    
    # Re-run metrics to automatically rebuild a fresh copy of the initial layout
    calculate_metrics()
    
    return {"status": "SUCCESS", "message": "Hotel layout reset back to default!"}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Renders the Receptionist Dashboard showing live room statuses."""
    
    # Fetch our newly calculated live JSON stats (re-reads your room_inventory.json every refresh!)
    stats = calculate_metrics()
    
    context = {
        "request": request, 
        "hotel_rooms": stats["hotel_rooms"],
        "room_types": [e.value for e in RoomType],
        "global_stats": stats["global"],         
        "type_stats": stats["by_type"],         
        "floor_stats": stats["by_floor"]        
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
    
    # 2. Check logic safety criteria up-front (P and V constraints)
    if not has_id: 
        return {"status": "DENIED", "message": "Booking Denied: Guest Identity Unverified (P failed)"}
    if not payment_verified: 
        return {"status": "DENIED", "message": "Booking Denied: Payment Processing Failed (V failed)"}
        
    # 3. Process the reservation directly inside your real JSON-backed database file
    result = reserve_room(room_type.value)
    
    if result["success"]:
        return {
            "status": "APPROVED",
            "message": f"Booking successful for {guest_name}!",
            "room_id": result["room_id"],
            "floor": result["floor"]
        }
    else:
        return {
            "status": "DENIED",
            "message": f"Booking Denied: {result['error']} (A empty)"
        }