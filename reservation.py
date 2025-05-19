
from datetime import datetime

class Reservation:
    def __init__(self, room, guest, check_in: str, check_out: str):
        self.room = room
        self.guest = guest
        self.check_in = self._parse_date(check_in)
        self.check_out = self._parse_date(check_out)
        self._active = True

    def _parse_date(self, date_str: str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD.")

    def cancel(self):
        if not self._active:
            print(f"Reservation for room {self.room.room_number} is already cancelled.")
        else:
            self._active = False
            print(f"Reservation for room {self.room.room_number} cancelled.")

    def __repr__(self):
        status = 'Active' if self._active else 'Cancelled'
        return (f"Reservation(Room {self.room.room_number}, Guest: {self.guest.name}, "
                f"{self.check_in} to {self.check_out}, Status: {status})")