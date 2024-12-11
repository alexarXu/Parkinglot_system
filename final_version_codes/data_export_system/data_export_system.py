import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import pandas as pd
import os


class DataExportImport:
    '''
    Data export/import class

    Attributes:
    root: The main window
    parking_records: A list of parking records
    history_records: A list of history records

    Methods:
    export_import_data: Display the data export/import menu
    export_parking_records: Export parking records
    export_history_records: Export history records
    import_records: Import records
    '''

    def __init__(self, root, parking_records, history_records):
        self.root = root
        self.parking_records = parking_records
        self.history_records = history_records

    def export_import_data(self):
        '''
        This method displays the data export/import menu.
        '''
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text="Data Export/Import",
            font=(
                "Times New Roman",
                18)).pack(
            pady=10)

        tk.Button(self.root, text="Export Parking Records", font=("Times New Roman", 14),
                  command=self.export_parking_records).pack(pady=10)
        tk.Button(self.root, text="Export History Records", font=("Times New Roman", 14),
                  command=self.export_history_records).pack(pady=5)
        tk.Button(self.root, text="Import Parking Records", font=("Times New Roman", 14),
                  command=lambda: self.import_records("parking")).pack(pady=5)
        tk.Button(self.root, text="Import History Records", font=("Times New Roman", 14),
                  command=lambda: self.import_records("history")).pack(pady=5)

    def export_parking_records(self):
        '''
        This method exports the parking records to an Excel file.
        '''
        if self.parking_records == {}:
            messagebox.showerror("Error", "No parking records to export.")
            return
        try:
            df = pd.DataFrame(
                self.parking_records, columns=[
                    "License Plate", "Entry Time"])
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                     filetypes=[("Excel Files", "*.xlsx")])
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo(
                    "Success", "Parking records exported successfully.")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to export parking records: {e}")

    def export_history_records(self):
        '''
        This method exports the history records to an Excel file.
        '''
        if self.history_records == []:
            messagebox.showerror("Error", "No history records to export.")
            return
        try:
            df = pd.DataFrame(
                self.history_records,
                columns=[
                    "License Plate",
                    "Entry Time",
                    "Exit Time",
                    "Fee"])
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                     filetypes=[("Excel Files", "*.xlsx")])
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo(
                    "Success", "History records exported successfully.")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to export history records: {e}")

    def import_records(self, record_type):
        '''
        This method imports records from an Excel or CSV file.
        '''
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Excel Files", "*.xlsx"), ("CSV Files", "*.csv")])
            if file_path:
                if file_path.endswith(".csv"):
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path)
                if record_type == "parking":
                    self.parking_records.extend(df.values.tolist())
                elif record_type == "history":
                    self.history_records.extend(df.values.tolist())
                messagebox.showinfo(
                    "Success", f"Records imported successfully into {record_type} records.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import records: {e}")
