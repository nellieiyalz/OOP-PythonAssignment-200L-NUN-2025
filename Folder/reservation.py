from room import HotelRoom
from guest import Guest

class Reservation(object):  
    def __init__(self, room: HotelRoom, guest: Guest,check_in_date, check_out_date):
        self.room = room
        self.guest = guest
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.active = True

    def __str__(self):
        return f"Reservation for {self.guest.name} in room {self.room.room_number} from {self.check_in_date} to {self.check_out_date}"
    
    def book_reservation(self):
        self.room.availibility = True
        pass


    def cancel_reservation(self):
        if self.active:
            self.active = False
            self.room.availibility = True
            return f"The reservation for {self.guest.name} in {self.room.room_number} at {self.check_in_date} has been canceled"
        return f"This reservation has already been canceled."
