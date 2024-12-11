import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import json
import os
from PIL import Image, ImageTk
from user_system.usr_manage_system import UserSystem
from car_system.car_manage_system import ParkingLotSystem
from data_export_system.data_export_system import DataExportImport

class MainMenuApp:
    '''
    Main menu class

    Attributes:
    root: The main window
    user_system: The user system object
    logged_in: A boolean indicating if the user is logged in
    car_system: The car management system object
    data_export_system: The data export/import system object

    Methods:
    create_main_menu: Create the main menu
    after_login: Callback after successful login
    car_management: Car management function
    export_data: Export data placeholder
    logout: Logout function
    '''
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to the Parking lot Management System!")
        self.user_system = UserSystem(root, self.create_main_menu)
        self.logged_in = False
        self.car_system = ParkingLotSystem(root)
        self.data_export_system = DataExportImport(root, self.car_system.parking_records, self.car_system.history_records)
        self.create_main_menu()

    def create_main_menu(self):
        '''
        This method creates the main menu, which is the first screen the user sees when they open the application.
        '''
        self.user_system.clear_frame()
        tk.Label(self.root, text="Main Menu", font=("Times New Roman", 18)).pack(pady=20)
        if not self.logged_in:
            tk.Button(self.root, text="User Login", font=("Times New Roman", 14), 
                      command=lambda: self.user_system.login_screen(self.after_login)).pack(pady=10)
        else:
            tk.Button(self.root, text="Car Management", font=("Times New Roman", 14), 
                      command=self.car_management).pack(pady=10)
            tk.Button(self.root, text="Export Data", font=("Times New Roman", 14), 
                      command=self.export_data).pack(pady=10)
            tk.Button(self.root, text="Logout", font=("Times New Roman", 14), 
                      command=self.logout).pack(pady=10)
        if not self.logged_in:
            tk.Button(self.root, text="Exit", font=("Times New Roman", 14), command=self.root.quit).pack(pady=10)

        image_frame = tk.Frame(self.root)
        image_frame.pack(pady=10)
        image = Image.open("C:/Users/administer/Desktop/SC/Campus-Navigation-System/car.png")
        photo = ImageTk.PhotoImage(image)
        img_label = tk.Label(image_frame, image=photo)
        img_label.image = photo 
        img_label.pack()


    def after_login(self):
        '''
        This method is called after the user has successfully logged in.
        '''
        self.logged_in = True
        self.create_main_menu()


    def car_management(self):
        '''
        This method displays the car management screen. Using the ParkingLotSystem class, the user can manage the parking lot.
        '''
        self.car_system.manage_screen()
        tk.Button(self.root, text="Back to Main Menu", font=("Times New Roman", 14), 
                  command=self.create_main_menu).pack(pady=10)
        

    def export_data(self):
        '''
        This method displays the data export/import screen. Using the DataExportImport class, the user can export and import parking records.
        '''
        self.data_export_system.export_import_data()
        tk.Button(self.root, text="Back to Main Menu", font=("Times New Roman", 14), 
                  command=self.create_main_menu).pack(pady=10)
    
    def logout(self):
        '''
        This method allows the user to logout of the system.
        '''
        self.logged_in = False
        messagebox.showinfo("Logout", "You have been logged out successfully.")
        self.create_main_menu()




if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x800")
    app = MainMenuApp(root)
    root.mainloop()
