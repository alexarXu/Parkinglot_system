import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
import json
import os
from PIL import Image, ImageTk
import base64
from user_system.encrypt_decrypt import encrypt_message, decrypt_message, load_keys

class UserSystem:
    '''
    UserSystem class for user management system

    Attributes:
    root: root window
    main_menu_callback: callback function to main menu
    users_file: JSON file to store user information
    admin_file: JSON file to store admin information
    users: dictionary to store user information
    admin: dictionary to store admin information

    Methods:
    load_admin: Load admin from a JSON file
    load_users: Load users from a JSON file
    save_users: Save users to a JSON file
    login_screen: User login screen
    verify_admin_password: Verify admin password
    login: Login function
    '''
    def __init__(self, root, main_menu_callback):
        self.root = root
        self.main_menu_callback = main_menu_callback
        self.users_file = 'user_info_data/users.json'
        self.admin_file = 'user_info_data/admin.json'
        self.load_users()
        self.load_admin()


    def load_admin(self):
        '''
        This method loads the admin information from a JSON file.
        '''
        if os.path.exists(self.admin_file):
            with open(self.admin_file, 'r') as file:
                self.admin = json.load(file)
        else:
            self.admin = {}


    def load_users(self):
        '''
        This method loads the user information from a JSON file.
        '''
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                self.users = json.load(file)
        else:
            # messagebox.showinfo("Actions needed", "No users found. Please register first!")
            self.users = {}


    def save_users(self):
        '''
        This method saves the user information to a JSON file.
        '''
        with open(self.users_file, 'w') as file:
            json.dump(self.users, file)


    def login_screen(self, callback=None):
        '''
        This method creates the login screen for the user management system.
        '''
        self.clear_frame()
        self.callback = callback

        tk.Label(self.root, text="User Login System", font=("Times New Roman", 18)).pack(pady=20)
        tk.Label(self.root, text="Username:", font=("Times New Roman", 12)).pack()
        self.username_entry = tk.Entry(self.root, font=("Times New Roman", 12))
        self.username_entry.pack()
        tk.Label(self.root, text="Password:", font=("Times New Roman", 12)).pack()
        self.password_entry = tk.Entry(self.root, show="*", font=("Times New Roman", 12))
        self.password_entry.pack()
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Login", font=("Times New Roman", 12), command=self.login).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Forgot Password?", font=("Times New Roman", 12), 
                  command=self.forgot_password_screen).pack(side=tk.LEFT, padx=5)
        tk.Button(self.root, text="Register", font=("Times New Roman", 12), 
                  command=self.verify_admin_password).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", font=("Times New Roman", 12), 
                  command=self.main_menu_callback).pack(pady=10)


    def verify_admin_password(self):
        '''
        This method verifies the admin password before allowing the user to register a new user.
        '''
        admin_password = simpledialog.askstring("Admin", "Enter admin password:", show='*') 
        private_key, _ = load_keys()      
        encrypted_password = self.admin["admin"]["password"]
        decrypted_password = decrypt_message(encrypted_password, private_key)

        if admin_password == None:
            return
        if decrypted_password == admin_password:
            self.register_screen()
        else:
            messagebox.showerror("Error", "Incorrect admin password")
    

    def login(self):
        '''
        This method verifies the user login credentials.
        '''
        if self.users == {}: 
            messagebox.showinfo("Actions needed", "No users found. Please register first!")
            return
        username = self.username_entry.get()
        password = self.password_entry.get()
        private_key, _ = load_keys()
        encrypted_password = self.users[username]["password"]
        decrypted_password = decrypt_message(encrypted_password, private_key)
        if username in self.users and decrypted_password == password:
            if self.callback:
                self.callback()
            messagebox.showinfo("Info", "Login successful!")
        else:
            messagebox.showerror("Error", "Invalid username or password! Please try again or register first!")


    def register_screen(self):
        '''
        This method creates the user registration screen.
        '''
        self.clear_frame()
        messagebox.showinfo("Successful verified!", "Proceed to register a new user.")
        tk.Label(self.root, text="User Registration System", font=("Times New Roman", 18)).pack(pady=20)
        tk.Label(self.root, text="Username:", font=("Times New Roman", 12)).pack()
        self.new_username_entry = tk.Entry(self.root, font=("Times New Roman", 12))
        self.new_username_entry.pack()
        tk.Label(self.root, text="Password (at least 6 characters):", font=("Times New Roman", 12)).pack()
        self.new_password_entry = tk.Entry(self.root, show="*", font=("Times New Roman", 12))
        self.new_password_entry.pack()
        tk.Label(self.root, text="Confirm Password:", font=("Times New Roman", 12)).pack()
        self.confirm_password_entry = tk.Entry(self.root, show="*", font=("Times New Roman", 12))
        self.confirm_password_entry.pack()
        tk.Label(self.root, text="Security Question:", font=("Times New Roman", 12)).pack()
        self.security_question_var = tk.StringVar(self.root)
        self.security_question_var.set("Select a question")
        security_questions = ["What is your pet's name?", "Where were you born?"]
        self.security_question_menu = tk.OptionMenu(self.root, self.security_question_var, *security_questions)
        self.security_question_menu.config(font=("Times New Roman", 12))
        self.security_question_menu.pack()
        tk.Label(self.root, text="Answer:", font=("Times New Roman", 12)).pack()
        self.security_answer_entry = tk.Entry(self.root, font=("Times New Roman", 12))
        self.security_answer_entry.pack()
        tk.Button(self.root, text="Register", font=("Times New Roman", 12), command=self.register).pack(pady=10)
        tk.Button(self.root, text="Back to Login", font=("Times New Roman", 12), 
                  command=lambda: self.login_screen(self.callback)).pack(pady=10)


    def register(self):
        '''
        This method registers a new user.
        '''
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        security_question = self.security_question_var.get()
        security_answer = self.security_answer_entry.get()
        _, public_key = load_keys()
        if username in self.users:
            messagebox.showerror("Error", "Username already existed!")
            return
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long!")
            return
        if password == confirm_password:
            if username and password and security_question != "Select a question" and security_answer:
                encrypted_password = encrypt_message(password, public_key)
                encrypted_security_answer = encrypt_message(security_answer, public_key)
                self.users[username] = {
                    "password": encrypted_password,
                    "security_question": security_question,
                    "security_answer": encrypted_security_answer
                }
                self.save_users()
                messagebox.showinfo("Info", "Registration successful!")
                self.login_screen(self.callback)
            else:
                messagebox.showerror("Error", "All fields are required!")
        else:
            messagebox.showerror("Error", "Passwords do not match!")


    def forgot_password_screen(self):
        '''
        This method creates the forgot password screen.
        '''
        self.clear_frame()
        tk.Label(self.root, text="Reset Password System", font=("Times New Roman", 18)).pack(pady=20)
        tk.Label(self.root, text="Username:", font=("Times New Roman", 12)).pack()
        self.reset_username_entry = tk.Entry(self.root, font=("Times New Roman", 12))
        self.reset_username_entry.pack()
        tk.Label(self.root, text="Security Question:", font=("Times New Roman", 12)).pack()
        self.security_question_var = tk.StringVar(self.root)
        self.security_question_var.set("Select a question")
        security_questions = ["What is your pet's name?", "Where were you born?"]
        self.security_question_menu = tk.OptionMenu(self.root, self.security_question_var, *security_questions)
        self.security_question_menu.config(font=("Times New Roman", 12))
        self.security_question_menu.pack()
        tk.Label(self.root, text="Answer:", font=("Times New Roman", 12)).pack()
        self.security_answer_entry = tk.Entry(self.root, font=("Times New Roman", 12))
        self.security_answer_entry.pack()
        tk.Button(self.root, text="Verify", font=("Times New Roman", 12), command=self.verify_security_answer).pack(pady=10)
        tk.Button(self.root, text="Back to Login", font=("Times New Roman", 12), 
                  command=lambda: self.login_screen(self.callback)).pack(pady=10)


    def verify_security_answer(self):
        '''
        This method verifies the security question and answer before allowing the user to reset the password.
        '''
        username = self.reset_username_entry.get()
        security_question = self.security_question_var.get()
        security_answer = self.security_answer_entry.get()
        
        if username in self.users:
            user_data = self.users[username]
            private_key, _ = load_keys()
            encrypted_security_answer = user_data["security_answer"]
            decrypted_security_answer = decrypt_message(encrypted_security_answer, private_key)
            if user_data["security_question"] == security_question and decrypted_security_answer == security_answer:
                self.show_reset_password_fields()
            else:
                messagebox.showerror("Error", "Security question or answer is incorrect!")
        else:
            messagebox.showerror("Error", "Username not found!")


    def show_reset_password_fields(self):
        '''
        This method shows the reset password fields.
        '''
        tk.Label(self.root, text="New Password:", font=("Times New Roman", 12)).pack()
        self.new_password_entry = tk.Entry(self.root, show="*", font=("Times New Roman", 12))
        self.new_password_entry.pack()
        tk.Label(self.root, text="Confirm New Password:", font=("Times New Roman", 12)).pack()
        self.confirm_new_password_entry = tk.Entry(self.root, show="*", font=("Times New Roman", 12))
        self.confirm_new_password_entry.pack()

        tk.Button(self.root, text="Reset Password", font=("Times New Roman", 12), 
                  command=self.reset_password).pack(pady=10)


    def reset_password(self):
        '''
        This method allows the user to reset the password.
        '''
        username = self.reset_username_entry.get()
        new_password = self.new_password_entry.get()
        confirm_new_password = self.confirm_new_password_entry.get()
        private_key, public_key = load_keys()

        if new_password == confirm_new_password:
            encrypted_new_password = encrypt_message(new_password, public_key)            
            encrypted_old_password = self.users[username]["password"]
            decrypted_old_password = decrypt_message(encrypted_old_password, private_key)
            
            if new_password == decrypted_old_password:
                messagebox.showerror("Error", "New password cannot be the same as the old password!")
            else:
                self.users[username]["password"] = encrypted_new_password
                self.save_users()
                messagebox.showinfo("Info", "Password reset successful!")
                self.login_screen(self.callback)
        else:
            messagebox.showerror("Error", "Passwords do not match!")


    def clear_frame(self):
        '''
        This method clears the frame.
        '''
        for widget in self.root.winfo_children():
            widget.destroy()