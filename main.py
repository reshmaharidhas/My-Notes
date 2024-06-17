import os
import My_Notes_App
import tkinter as tk
from tkinter import messagebox

# Function to validate the user entered login credentials by comparing the user id and password of MySQL database using Environment variables
def validate():
    try:
        if (host_var.get()=="127.0.0.1" and username_var.get()==os.getenv('MYSQL_USER') and server_password_var.get()==os.getenv('MYSQL_PASSWORD')):
            window.destroy()
            My_Notes_App.My_Notes_App(host_var.get(),username_var.get(),server_password_var.get())
        else:
            messagebox.showerror("Invalid credentials","Wrong details entered. Please enter the correct details!")
    except Exception as err:
        messagebox.showerror("Empty credentials","Please enter all the details to login")

if __name__ == '__main__':
    # GUI
    window = tk.Tk()
    window.title("My Notes - Enter login credentials")
    window.geometry("400x280")
    window.minsize(width=400,height=280)
    window.config(bg="turquoise")
    # variables
    host_var = tk.StringVar()
    username_var = tk.StringVar()
    server_password_var = tk.StringVar()
    app_logo_icon = tk.PhotoImage(file="logo.png")
    # widgets
    tk.Label(window,text="Enter hostname:",font=("Arial",14),bg="turquoise").pack(pady=7)
    entry_hostname = tk.Entry(window,textvariable=host_var,font=("Arial",13),bd=2)
    entry_hostname.pack(pady=2)
    tk.Label(window,text="Enter user id:",font=("Arial",14),bg="turquoise").pack(pady=5)
    entry_username = tk.Entry(window,textvariable=username_var,font=("Arial",14),bd=2)
    entry_username.pack(pady=5)
    tk.Label(window,text="Enter password:",font=("Arial",14),bg="turquoise").pack(pady=5)
    entry_password = tk.Entry(window,textvariable=server_password_var,font=("Arial",14),bd=2,show="*")
    entry_password.pack(pady=5)
    connect_button = tk.Button(window,text="Connect",command=validate,font=("Times New Roman",16),bg="blue",fg="white",activebackground="blue",activeforeground="yellow")
    connect_button.pack(pady=10)
    window.iconphoto(True, app_logo_icon)
    window.mainloop()
