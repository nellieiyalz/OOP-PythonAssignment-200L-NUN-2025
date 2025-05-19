from pydoc import text
from sqlite3 import Date
from tkinter import messagebox
from turtle import width
from guest import Guest
from reservation import Reservation
from room import HotelRoom
import json
import tkinter as tk
from tkinter import *
from tkinter import simpledialog
from tkinter import Tk
from tkinter import ttk
import datetime

import room

### Important notes
# Docstrings give relevant information on functions so when you hover over them with your mouse you can see the information given
# they are defined with triple quotes """Information here"""

class HotelManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("600x600")
        self.create_widgets()
        self.database = self.load_from_file()
        self.rooms = self.database.get('rooms', [])
        self.reservations = self.database.get('reservations', {})
        self.configure_tree_view()
        self.room_tree_view.bind("<<TreeviewSelect>>", self.on_tree_select) # Binds the on_tree_select function to the main tree view 
        self.selected_room_number = None

    def create_widgets(self):
        """Handles the initial creation of all the gui elements."""
        self.create_room_button = ttk.Button(self.root, text="Add Room", width=60, command=self.request_room_info)
        self.book_reservation_button = ttk.Button(self.root, text="Book Reservation", width=60, command=self.request_reservation_info)
        self.check_in_guest_button = ttk.Button(self.root, text="Check In", width=60, command=self.request_check_in_info)
        self.check_out_guest_button = ttk.Button(self.root, text="Check Out", width=60, command=self.request_check_out_info)
        self.cancel_reservation_button = ttk.Button(self.root, text="Cancel Reservation", width=60, command=self.request_cancel_info)
        self.room_tree_view = ttk.Treeview(self.root, selectmode='browse')

        self.create_room_button.grid(row=1, column=0,padx=5, pady=5)
        self.book_reservation_button.grid(row=2, column=0, padx=5, pady=5)
        self.cancel_reservation_button.grid(row=3, column=0, padx=5, pady=5)
        self.check_in_guest_button.grid(row=4, column=0, padx=5, pady=5)
        self.check_out_guest_button.grid(row=5, column=0, padx=5, pady=5)
        

        self.room_tree_view.grid(row=0, column=0, padx=5, pady=5)

        self.room_tree_view["columns"] = ("1", "2", "3", "4")
        self.room_tree_view['show'] = 'headings'

        self.room_tree_view.column("1", width=90, anchor='c')
        self.room_tree_view.column("2", width=90, anchor='se')
        self.room_tree_view.column("3", width=90, anchor='se')
        self.room_tree_view.column("4", width=90, anchor='se')

        self.room_tree_view.heading("1", text="Number")
        self.room_tree_view.heading("2", text="Type")
        self.room_tree_view.heading("3", text="Price")
        self.room_tree_view.heading("4", text="Available")

    def configure_tree_view(self):
        for room in self.rooms:
            self.room_tree_view.insert("", 0, text="L10", values=(room['room_number'], room['room_type'], room['price'], room['availibility'],))

    def on_tree_select(self, event):
        selected_items = self.room_tree_view.selection()
        if selected_items:
            selected_item = selected_items[0]
            room_values = self.room_tree_view.item(selected_item, 'values')
            if room_values:
                self.selected_room_number = int(room_values[0])
                room = self.get_room(self.selected_room_number)
                if room:
                    pass
            else: 
                self.selected_room_number = None
        else:
            self.selected_room_number = None


    def load_from_file(self):
        try:
            with open("database.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {'rooms': [], 'reservations': {}} # Return an empty list if the file doesn't exist yet to prevent a crash.
        except json.JSONDecodeError:
            return {'rooms': [], 'reservations': {}} # Return an empty list if the file is corrupted to prevent a crash.

    def save_to_file(self):
        self.database['rooms'] = self.rooms
        self.database['reservations'] = self.reservations
        try:
            with open("database.json", "w") as file:
                json.dump(self.database, file)
        except IOError as e:
            messagebox.showerror("File Error", f"Could not save data: {e}") # Log the error
        pass

    def parse_date(self, date_str):
        """Parses a string in DD/MM/YYYY formate to a datetime object to avoid issues"""
        try:
            day, month, year = map(int, date_str.split('/'))
            return datetime.date(year, month, day)
        except ValueError:
            return None
        
    def date_to_str(self, date_obj):
        """Converts a date object to a string"""
        if isinstance(date_obj, datetime.date):
            return date_obj.strftime("%d/%m/%Y")
        return str(date_obj)

    def request_reservation_info(self):
        if self.selected_room_number is None:
            messagebox.showerror("Error", "Please select a room first.")
            return
        else:
            check_in_date = Date.today()
            guest_name = simpledialog.askstring("Guest Info", "Enter the guests name.")
            if guest_name is None:
                messagebox.showerror("Invalid Input", "Guest name can only be a string.")
                return
            
            guest_contact_info = simpledialog.askstring("Guest Info", "Enter the guests contact info.")
            if guest_contact_info is None:
                messagebox.showerror("Invalid Input", "Contact info can only be a int.")
                return
            
            check_out_date = simpledialog.askstring("Guest Info", "When will the guest be checking out"
            "Please input a valid date in the format DD/MM/YYYY. ")
            if check_out_date is None:
                messagebox.showerror("Invalid Input", "Please input a valid date in the format DD/MM/YYYY.")
                return
            
            current_guest = {
                "name": guest_name,
                "contact_info": guest_contact_info,
                "checked_in": False
            }
            self.book_room(self.selected_room_number, current_guest, check_in_date, check_out_date)

    def request_check_in_info(self):
        """Request information needed to check a guest in."""
        if self.selected_room_number is None:
            messagebox.showerror("Error", "Please select a room first.")
            return
        
        # Check if the reservation exists
        reservation_id = None
        for res_id, res in self.reservations.items():
            if res["room_number"] == self.selected_room_number:
                reservation_id = res_id
                break

        if not reservation_id:
            messagebox.showerror("Error", f"No reservation found for room{self.selected_room_number}")
            return
        
        if self.reservations[reservation_id]["checked_in"]:
            messagebox.showerror("Error", f"Guest already checked in to room {self.selected_room_number}.")
            return
        
        # Get guest information
        guest_name = simpledialog.askstring("Guest Info", "Enter the guest's name")
        if guest_name is None:
            messagebox.showerror("Error", "Please input a guest name.")
            return
        
        guest_contact_info = simpledialog.askstring("Guest Info", "Enter the guest's contact info")
        if guest_contact_info is None:
            messagebox.showerror("Error", "Please input guest contact information.")
            return
        
        guest = {
            "name": guest_name,
            "contact_info": guest_contact_info
        }

        self.check_in_guest(self.selected_room_number, guest)

    def request_check_out_info(self):
        """Requests information needed to check out a guest."""
        if self.selected_room_number is None:
            messagebox.showerror("Error", "Please select a room first.")
            return
        
        confirm = messagebox.askyesno("Confirm Check-out", f"Are your sure you want to check out the guest form room {self.selected_room_number}?")

        if confirm:
            self.check_out_guest(self.selected_room_number)

    def request_cancel_info(self):
        """Requests information needed to cancel a reservation."""
        if self.selected_room_number is None:
            messagebox.showerror("Error", "Please select a room first.")
            return
        
        confirm = messagebox.askyesno("Confirm Cancellation", f"Are you sure you want to cancel the reservation for room {self.selected_room_number}?")

        if confirm:
            self.cancel_reservation(self.selected_room_number)

    def request_room_info(self):
        """Opens dialogs to get room details from the user using tkinter gui and adds the room to the json database."""

        room_number = simpledialog.askinteger("Add Room", "Enter room number")
        if room_number is None: 
            return
        
        room_type = simpledialog.askstring("Add Room", "Enter room type (e.g., Single, Double, Suite):")
        if room_type is None:  #Throws an error if one of the valid room types is not provided.
            return
        
        price = simpledialog.askfloat("Add Room", "Enter price per night: ")
        if price is None:
            return
        
        self.add_room(room_number, room_type, price)
        self.room_tree_view.delete(*self.room_tree_view.get_children())
        self.configure_tree_view()
        
    def add_room(self, room_number, room_type, price):
        """Adds a new room to the hotel database."""
        room_exists = any(room['room_number'] == room_number for room in self.rooms)
        
        if room_exists:
            messagebox.showerror("Error", f"Room {room_number} already exists.")
        else:
            new_room = {
                "room_number": room_number,
                "room_type": room_type,
                "price": price,
                "availibility": True
            }
            self.rooms.append(new_room)
            self.save_to_file()
            messagebox.showinfo("Success", f"Room {room_number} added successfully!")

    def get_room(self, room_number):
        """Retrieves a room by its number"""
        for room in self.rooms:
            if room["room_number"] == room_number:
                return room
        return None

    def book_room(self, room_number: int, guest, check_in_date, check_out_date):
        room = self.get_room(room_number)
        if not room:
            messagebox.showerror("Error", f"Room {room_number} does not exist.")
            return
        
        if not room["availibility"]:
            messagebox.showerror("Error", f"Room {room_number} has already been booked.")
            return
        
        room["availibility"] = False
        guest_dict = guest.__dict__ if hasattr(guest, "__dict__") else guest

        reservation_id = f"{room_number}_{self.date_to_str(check_in_date)}"

        self.reservations[reservation_id] = {
            "room_number": room_number,
            "guest": guest_dict,
            "check_in_date": self.date_to_str(check_in_date),
            "check_out_date": self.date_to_str(check_out_date),
            "checked_in": False
        }

        self.save_to_file()
        messagebox.showinfo("Success", f"Room {room_number} has been booked successfully!")

        self.room_tree_view.delete(*self.room_tree_view.get_children())
        self.configure_tree_view()

    def cancel_reservation(self, room_number: int):
        reservation_id = None
        for res_id, res in self.reservations.items():
            if res["room_number"] == room_number:
                reservation_id = res_id
                break

        if not reservation_id:
            messagebox.showerror("Error", f"No reservation found for room {room_number}.")
            return
        
        room = self.get_room(room_number)
        if room:
            room["availibility"] = True

        del self.reservations[reservation_id] # Delete the reservation found using the reservation id
        self.save_to_file()
        messagebox.showinfo("Success", f"Reservation for room {room_number} cancelled!")

        self.room_tree_view.delete(*self.room_tree_view.get_children())
        self.configure_tree_view()

    def check_in_guest(self, room_number, guest):
        reservation_id = None
        for res_id, res in self.reservations.items():
            if res["room_number"] == room_number:
                reservation_id = res_id
                break

        if reservation_id is None:
            messagebox.showerror("Error", f"No reservation found for room {room_number}.")
            return
        
        self.reservations[reservation_id]["checked_in"] = True

        if guest:
            guest_dict = guest.__dict__ if hasattr(guest, "__dict__") else guest
            self.reservations[reservation_id]["guest"] = guest_dict

        self.save_to_file()
        messagebox.showinfo("Success", f"Guest checked into room {room_number}!")

    def check_out_guest(self, room_number):
        reservation_id = None
        for res_id, res in self.reservations.items():
            if res["room_number"] == room_number:
                reservation_id = res_id
                break

        if not reservation_id or not self.reservations[reservation_id]["checked_in"]:
            messagebox.showerror("Error", f"No checked-in guest found for room {room_number}.")
            return
        
        room = self.get_room(room_number)
        if room:
            room["availibility"] = True

        del self.reservations[reservation_id]
        self.save_to_file()
        messagebox.showinfo("Success", f"Guest checked out from room {room_number}")

        self.room_tree_view.delete(*self.room_tree_view.get_children())
        self.configure_tree_view()

root = Tk()
app = HotelManagement(root)
root.mainloop()