import json
import os
from typing import Dict, Any

DB_FILE = "room_inventory.json"

def get_initial_data() -> Dict[str, list]:
    try:
        from data import HOTEL_ROOMS
        return {str(floor): rooms for floor, rooms, in HOTEL_ROOMS.items()}
    except ImportError:
        return {
            "1": [
                {"id": 101, "type": "Family", "is_occupied": False},
                {"id": 102, "type": "Family", "is_occupied": True},
                {"id": 103, "type": "Balcony", "is_occupied": False},
            ],
            "2": [
                {"id": 201, "type": "Balcony", "is_occupied": False},
                {"id": 202, "type": "Suite", "is_occupied": False},
            ],
            "3": [
                {"id": 301, "type": "Suite", "is_occupied": False},
                {"id": 302, "type": "Suite", "is_occupied": True},
            ]
        }
    
def load_inventory() -> Dict[str, list]:
    if not os.path.exists(DB_FILE):
        initial_data = get_initial_data()
        save_inventory(initial_data)
        return initial_data
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        initial_data = get_initial_data()
    return initial_data

def save_inventory(data: Dict[str, list]):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)
        
def calculate_metrics() -> Dict[str, Any]:
    hotel_data = load_inventory()
    
    total_room = 0
    total_occupied = 0
    
    type_stats = {}
    floor_stats = {}
    
    for floor_str, rooms in hotel_data.items():
        floor_num = int(floor_str)
        
        if floor_num not in floor_stats:
            # FIXED: Changed "ocuppied" to "occupied" to match index.html properties
            floor_stats[floor_num] = {"total" : 0, "occupied" : 0, "available" : 0}
        
        for room in rooms:
            total_room += 1
            floor_stats[floor_num]["total"] += 1
            
            rtype = room["type"]
            if rtype not in type_stats:
                # FIXED: Changed "ocuppied" to "occupied"
                type_stats[rtype] = {"total" : 0, "occupied" : 0, "available" : 0}
            type_stats[rtype]["total"] += 1
            
            if room["is_occupied"]:
                total_occupied += 1
                floor_stats[floor_num]["occupied"] += 1
                type_stats[rtype]["occupied"] += 1
            else:
                floor_stats[floor_num]["available"] += 1
                type_stats[rtype]["available"] += 1
    
    occupancy_rate = round((total_occupied / total_room) * 100, 1) if total_room > 0 else 0.0
    
    return {
        "hotel_rooms": hotel_data,
        "global": {
            "total": total_room,
            "occupied": total_occupied,
            "available": total_room - total_occupied,
            "rate_percent": occupancy_rate
        },
        "by_type": type_stats,
        "by_floor": floor_stats
    }
    
# FIXED: Renamed function spelling from reseve_room to reserve_room
def reserve_room(room_type: str) -> Dict[str, Any]:
    hotel_data = load_inventory()
    
    for floor_str, rooms in hotel_data.items():
        for room in rooms:
            if room["type"] == room_type and not room["is_occupied"]: 
                room["is_occupied"] = True  # FIXED: Corrected spelling to match schema
                save_inventory(hotel_data)
                return {"success" : True, "room_id": room["id"], "floor": floor_str}
    return {"success": False, "error": f"No vacant {room_type} room available"}