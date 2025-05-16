class Guest:
    def __init__(self, name, contact_info):
        self.name = name
        self.contact_info = contact_info
        self.checked_in = False

    def checkIn(self):
        """Checks a guest into the hotel"""
        self.checked_in = True
        return f"{self.name} has checked in"

    def checkOut(self):
        """Checks a guest out of the hotel"""
        if self.checked_in:
            self.checked_in = False
            return f"{self.name} has checked out."
        return f"{self.name} is not checked in."
    
    def __str__(self):
        """"Returns a clean/sanitized string represantation of a guest"""
        status = "Checked in" if self.checked_in else "Not checked in"
        return f"Guest: {self.name}, Contact: {self.contact_info}, Status: {status}"
        