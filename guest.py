class Guest:
    def __init__(self, name: str, contact: str):
        self.name = name
        self.contact = contact
        self._checked_in = False

    def checked_in(self):
        if self._checked_in:
            print(f"{self.name} is already checked in.")
        else:
            self._checked_in = True
            print(f"{self.name} has checked in.")

    def checked_out(self):
        if not self._checked_in:
            print(f"{self.name} is not currently checked in.")
        else:
            self._checked_in = False
            print(f"{self.name} has checked out.")