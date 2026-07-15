# data.py

HOTEL_ROOMS = {
    1: [
        {"id": 101, "type": "Family", "is_occupied": False},
        {"id": 102, "type": "Family", "is_occupied": True}, # Started occupied to test logic
        {"id": 103, "type": "Balcony", "is_occupied": False},
    ],
    2: [
        {"id": 201, "type": "Balcony", "is_occupied": False},
        {"id": 202, "type": "Suite", "is_occupied": False},
    ],
    3: [
        {"id": 301, "type": "Suite", "is_occupied": False},
        {"id": 302, "type": "Suite", "is_occupied": True},
    ]
}