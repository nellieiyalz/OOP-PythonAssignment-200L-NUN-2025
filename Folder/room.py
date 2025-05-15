class HotelRoom(object):
    room_number = 0
    room_type = ""
    price = 0 
    availibility = True

    def __init__(self, room_number: int, room_type: str, price: int, availibility: bool):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.availibility = availibility

    def __repr__(self):
        return f"Room(room_number='{self.room_number}', room_type={self.room_number}, price={self.price})"

    def getRoomNumber(self):
        return self.room_number

    def getRoomPrice(self):
        return self.price
    
    def getRoomType(self): 
        return self.room_type

    def getRoomAvailibility(self):
        return self.availibility
    
