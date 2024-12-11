import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import random
import string
import hyperlpr3 as lpr3
import cv2
from PIL import Image, ImageTk
import csv

class ParkingLotSystem:
    '''
    This is a class for managing the parking lot system.

    Attributes:
    root: The root window of the application.
    parking_records: A dictionary to store the current parking records.
    history_records: A list to store the historical parking records.
    image_label: A label to display the uploaded image.

    Methods:
    clear_frame: Clear the current interface.
    manage_screen: Create the main interface of the parking lot system.
    upload_image: Handle the image upload logic.
    display_image: Display the uploaded image.
    simulate_plate_recognition: Simulate the license plate recognition from the image.
    vehicle_entry: Handle the vehicle entry logic.
    vehicle_exit: Handle the vehicle exit logic.
    view_parking_records: View the current parking records.
    view_history_records: View and manage the historical parking records.
    delete_history_record: Delete a specific historical record.
    save_parking_records: Save the current parking records to a CSV file.
    load_parking_records: Load the parking records from a CSV file.
    save_history_records: Save the historical parking records to a CSV file.
    load_history_records: Load the historical parking records from a CSV file.
    '''
    def __init__(self, root):
        self.root = root
        self.root.title("Parking Lot System")
        self.root.geometry("1000x800")

        self.parking_records = {}
        self.history_records = []  
        self.image_label = None 

        self.manage_screen()

        self.load_history_records()
        self.load_parking_records()


    def manage_screen(self):
        '''
        This method creates the main interface of the parking lot system.
        '''
        self.clear_frame()

        tk.Label(self.root, text="Parking Lot Management", font=("Times New Roman", 18)).pack(pady=20)
        tk.Button(self.root, text="Upload Image for Recognition", font=("Times New Roman", 14), command=self.upload_image).pack(pady=10)
        self.plate_entry = tk.Entry(self.root, font=("Times New Roman", 14), width=20)
        self.plate_entry.pack(pady=10)
        tk.Label(self.root, text="License Plate", font=("Times New Roman", 12)).pack()
        tk.Button(self.root, text="Vehicle Entry", font=("Times New Roman", 14), command=self.vehicle_entry).pack(pady=10)
        tk.Button(self.root, text="Vehicle Exit", font=("Times New Roman", 14), command=self.vehicle_exit).pack(pady=10)
        tk.Button(self.root, text="View Current Parking Records", font=("Times New Roman", 14), 
                  command=self.view_parking_records).pack(pady=10)
        tk.Button(self.root, text="View and Manage History Records", font=("Times New Roman", 14), 
                  command=self.view_history_records).pack(pady=10)


    def clear_frame(self):
        '''
        This method clears the current interface.
        '''
        for widget in self.root.winfo_children():
            widget.destroy()


    def display_image(self, file_path):
        '''
        This method displays the uploaded image in the interface.
        '''
        image = Image.open(file_path)
        image = image.resize((400, 300))
        img_tk = ImageTk.PhotoImage(image)

        if self.image_label:
            self.image_label.destroy()

        self.image_label = tk.Label(self.root, image=img_tk)
        self.image_label.image = img_tk  
        self.image_label.pack(pady=10)


    def upload_image(self):
        '''
        This method handles the image uploading.
        '''
        file_path = filedialog.askopenfilename(filetypes=[["Image Files", "*.png;*.jpg;*.jpeg"]])
        if file_path:
            self.display_image(file_path)
            recognized_plate = self.simulate_plate_recognition(file_path)
            if recognized_plate:
                self.plate_entry.delete(0, tk.END)
                self.plate_entry.insert(0, recognized_plate)
                messagebox.showinfo("Recognition Success", f"Recognized License Plate: {recognized_plate}")
            else:
                messagebox.showerror("Recognition Failed", "Failed to recognize license plate from the image.")


    def simulate_plate_recognition(self, file_path):
        '''
        This method simulates the license plate recognition from the image. 
        Use the hyperlpr3 library to recognize the license plate from the image.
        '''
        catcher = lpr3.LicensePlateCatcher()
        img = cv2.imread(file_path)
        chars = catcher(img)
        return chars[0][0] if chars else None


    def vehicle_entry(self):
        '''
        This method handles the vehicle entry.
        '''
        plate = self.plate_entry.get().strip()
        if not plate:
            messagebox.showerror("Error", "License plate cannot be empty!")
            return
        if plate in self.parking_records:
            messagebox.showerror("Error", "This vehicle is already in the parking lot!")
        else:
            self.parking_records[plate] = datetime.now()
            self.save_parking_records()
            messagebox.showinfo("Info", f"Vehicle {plate} entered at {self.parking_records[plate].strftime('%Y-%m-%d %H:%M:%S')}")


    def vehicle_exit(self):
        '''
        This method handles the vehicle exit.
        '''
        plate = self.plate_entry.get().strip()
        if not plate:
            messagebox.showerror("Error", "License plate cannot be empty!")
            return
        if plate not in self.parking_records:
            messagebox.showerror("Error", "This vehicle is not in the parking lot!")
        else:
            entry_time = self.parking_records.pop(plate)
            exit_time = datetime.now()
            duration = exit_time - entry_time
            hours = max(1, int(duration.total_seconds() // 3600))
            fee = hours * 5  # I set the parking fee as S5 per hour
            self.history_records.append((plate, entry_time, exit_time, fee))
            self.save_history_records()

            messagebox.showinfo("Exit Info", 
                                f"Vehicle {plate} exited at {exit_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                                f"Total time: {hours} hours\n"
                                f"Parking fee: ${fee}")
            

    def view_parking_records(self):
        '''
        This method displays the current parking records.
        '''
        if not self.parking_records:
            messagebox.showinfo("Parking Records", "No vehicles in the parking lot.")
            return
        record_window = tk.Toplevel(self.root)
        record_window.title("Parking Records")
        record_window.geometry("1000x800")
        tk.Label(record_window, text="Current Parking Records", font=("Times New Roman", 14)).pack(pady=10)
        for plate, entry_time in self.parking_records.items():
            tk.Label(record_window, text=f"Vehicle {plate} - Entered at {entry_time.strftime('%Y-%m-%d %H:%M:%S')}", 
                     font=("Times New Roman", 10)).pack(anchor="w", padx=10, pady=2)


    def view_history_records(self):
        '''
        This method displays the historical parking records.
        '''
        if not self.history_records:
            messagebox.showinfo("History Records", "No historical records available.")
            return
        history_window = tk.Toplevel(self.root)
        history_window.title("History Records")
        history_window.geometry("1000x800")
        tk.Label(history_window, text="Historical Parking Records", font=("Times New Roman", 14)).pack(pady=10)
        for idx, record in enumerate(self.history_records):
            plate, entry_time, exit_time, fee = record
            record_frame = tk.Frame(history_window)
            record_frame.pack(fill="x", padx=10, pady=5)

            tk.Label(record_frame, text=(f"{idx+1}. Vehicle {plate}: Entered at {entry_time.strftime('%Y-%m-%d %H:%M:%S')}, "
                                         f"Exited at {exit_time.strftime('%Y-%m-%d %H:%M:%S')}, Fee: ¥{fee}"),
                     font=("Times New Roman", 10)).pack(side="left")    
            tk.Button(record_frame, text="Delete", font=("Times New Roman", 10), 
                      command=lambda idx=idx: self.delete_history_record(idx)).pack(side="right")


    def delete_history_record(self, idx):
        '''
        This method allow users to delete a specific historical record.
        '''
        if idx < len(self.history_records):
            del self.history_records[idx]
            self.save_history_records()
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Toplevel) and widget.title() == "History Records":
                    widget.destroy()
            if not self.history_records:
                messagebox.showinfo("Info", "No historical records left.")
                return
            messagebox.showinfo("Info", "Record deleted successfully!")
            self.view_history_records()


    def save_parking_records(self):
        '''
        This method saves the current parking records to a CSV file.
        '''
        with open("/final_version_codes/data_storage/parking_records.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Plate", "Entry Time"])
            for plate, entry_time in self.parking_records.items():
                writer.writerow([plate, entry_time.strftime('%Y-%m-%d %H:%M:%S')])


    def load_parking_records(self):
        '''
        This method loads the parking records from a CSV file.
        '''
        try:
            with open("/final_version_codes/data_storage/parking_records.csv", mode="r", newline="") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    plate, entry_time = row
                    self.parking_records[plate] = datetime.strptime(entry_time, '%Y-%m-%d %H:%M:%S')
        except FileNotFoundError:
            pass  # If file not found, it means no records exist yet


    def save_history_records(self):
        '''
        This method saves the historical parking records to a CSV file.
        '''
        with open("/final_version_codes/data_storage/history_records.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Plate", "Entry Time", "Exit Time", "Fee"])
            for record in self.history_records:
                plate, entry_time, exit_time, fee = record
                writer.writerow([plate, entry_time.strftime('%Y-%m-%d %H:%M:%S'), 
                                 exit_time.strftime('%Y-%m-%d %H:%M:%S'), fee])


    def load_history_records(self):
        '''
        This method loads the historical parking records from a CSV file.
        '''
        try:
            with open("/final_version_codes/data_storage/history_records.csv", mode="r", newline="") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    plate, entry_time, exit_time, fee = row
                    entry_time = datetime.strptime(entry_time, '%Y-%m-%d %H:%M:%S')
                    exit_time = datetime.strptime(exit_time, '%Y-%m-%d %H:%M:%S')
                    self.history_records.append((plate, entry_time, exit_time, float(fee)))
        except FileNotFoundError:
            pass  # If file not found, it means no records exist yet
