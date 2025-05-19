
class Room:
    def __init__(self, room_number: int, room_type: str, price: float):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.available = True

    def __repr__(self):
        status = 'Available' if self.available else 'Booked'
        return f"Room {self.room_number}: {self.room_type}, ${self.price}, {status}"

