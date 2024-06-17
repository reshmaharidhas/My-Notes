import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

class My_Notes_App:
    def __init__(self,host_var,username_var,password_var):
        # GUI
        self.root = tk.Tk()
        self.root.geometry("1100x750")
        self.root.minsize(width=1100,height=750)
        self.root.title("My Notes")
        self.root.config(bg="turquoise")
        # PhotoImage variables
        self.delete_icon_image = tk.PhotoImage(file="delete_notes_image.png").subsample(2,2)
        self.refresh_icon_image = tk.PhotoImage(file="icons8-refresh-48.png").subsample(2,2)
        self.add_note_icon_image = tk.PhotoImage(file="icons8-add-48.png").subsample(2,2)
        self.edit_icon_image = tk.PhotoImage(file="icons8-edit-100.png").subsample(3,3)
        self.save_changes_icon_image = tk.PhotoImage(file="icons8-save-48.png").subsample(2,2)
        self.app_logo_icon = tk.PhotoImage(file="logo.png")
        # Menu bar
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        self.fileMenu = tk.Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label="File",menu=self.fileMenu)
        self.fileMenu.add_command(label="Add new note",command=self.add_to_gui)
        self.edit_Menu = tk.Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label="Edit",menu=self.edit_Menu)
        self.edit_Menu.add_command(label="Delete all notes",command=self.delete_all_notes)
        self.help_Menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.help_Menu)
        self.help_Menu.add_command(label="About", command=self.show_about)
        # Establishing database connection
        self.host_var = host_var
        self.username_var = username_var
        self.password_var = password_var
        # Establish connection to database and table
        self.connect_to_database()
        # UI
        self.buttons_frame = tk.Frame(self.root,background="turquoise")
        self.buttons_frame.pack(pady=9)
        self.btn_add = tk.Button(self.buttons_frame,text="Add new note",bg="blue",fg="white",font=("Arial",16),command=self.add_to_gui,image=self.add_note_icon_image,compound=tk.LEFT,padx=3)
        self.btn_add.grid(row=0,column=0,padx=10)
        self.btn_refresh = tk.Button(self.buttons_frame,text="Refresh notes",bg="green",fg="white",font=("Arial",16),command=self.refresh_updated_data,image=self.refresh_icon_image,compound=tk.LEFT,padx=3)
        self.btn_refresh.grid(row=0,column=1)
        self.btn_save_changes = tk.Button(self.buttons_frame,text="Save",bg="purple",fg="white",font=("Arial",16),command=self.save_changes_to_table,state=tk.DISABLED,image=self.save_changes_icon_image,compound=tk.LEFT,padx=5)
        self.btn_save_changes.grid(row=0,column=2,padx=7)
        self.textarea = tk.Text(self.root,width=60,height=5,borderwidth=2)
        self.textarea.pack(pady=10)
        self.container = tk.Frame(self.root,background="turquoise")
        self.canvas = tk.Canvas(self.container,width=770,height=550)
        self.canvas.configure(bg="#70a1ff")
        self.scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas,background="#70a1ff")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.container.pack(pady=2)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.global_id = 0
        self.root.iconphoto(True,self.app_logo_icon)
        self.refresh_updated_data()
        self.root.mainloop()

    def connect_to_database(self):
        # Establishing database connection
        self.db = mysql.connector.connect(host=self.host_var,
                                          user=self.username_var,
                                          passwd=self.password_var)
        self.my_cursor = self.db.cursor()
        # Check whether database is present or not.
        self.my_cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'my_notes_db';")
        self.answer = self.my_cursor.fetchone()
        if self.answer:
            pass
        else:
            self.my_cursor.execute("CREATE DATABASE my_notes_db;")
        self.my_cursor.execute("USE my_notes_db;")
        self.database_name_var = "my_notes_db"
        # Check if there is table 'my_notes_app' present in database 'my_notes_db'.
        # If there is no such table, create table.
        try:
            self.my_cursor.execute("SELECT * FROM my_notes_app;")
            table_rows = self.my_cursor.fetchall()
        except Exception as err:
            self.my_cursor.execute("CREATE TABLE my_notes_app (id int NOT NULL AUTO_INCREMENT,notes_content VARCHAR(255),PRIMARY KEY (id));")


    # Function to insert the user typed content in Text widget to the table 'my_notes_app'.
    def add_to_gui(self):
        try:
            content_typed = self.textarea.get(1.0, tk.END)
            if len(content_typed) > 1:
                formula = "INSERT INTO my_notes_app (notes_content) VALUES (%s)"
                self.my_cursor.execute(formula, (content_typed, ))
                self.db.commit()
                # Refresh the canvas.
                self.refresh_updated_data()
                self.btn_save_changes.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error occurred","Unable to insert to database")

    # Function to delete the selected note from your notes.
    def delete_selected_note_from_database(self,event):
        try:
            # Get the text inside the Text widget
            row_selected = int(event.widget.cget('text'))
            # Ask confirmation before deleting the note from user.
            # If user select 'YES', delete the note.
            if messagebox.askyesno("Delete note?", "Do you really want to delete this note?"):
                # Run the query to delete the row
                self.my_cursor.execute(f"DELETE FROM my_notes_app WHERE id={row_selected};")
                # Make sure to commit() to save the changes. Otherwise, that row is not deleted completely.
                self.db.commit()
                self.refresh_updated_data()
        except:
            messagebox.showerror("Error", "Unable to delete note from database!")


    # Function to edit the selected note from all your notes fetched from table 'my_notes_app'.
    def edit_note_in_textarea(self,event):
        global global_id
        try:
            self.textarea.delete(1.0, tk.END)
            row_id = int(event.widget.cget('text'))
            self.my_cursor.execute(f"SELECT notes_content FROM my_notes_app WHERE id={row_id}")
            result = self.my_cursor.fetchone()[0]
            self.textarea.insert(tk.END, result)
            self.btn_save_changes.grid(row=0, column=2, padx=8)
            self.global_id = row_id
            self.btn_save_changes.config(state=tk.NORMAL)
        except:
            messagebox.showerror("Error", "Error during updating!")

    # Function to save the modified content to the table if the id of the selected row exists in the table.
    def save_changes_to_table(self):
        global global_id
        # Checking if a row with id=global_id exists before making update.
        # If present, it returns a tuple containing integer 1. Otherwise the tuple contains integer 0.
        self.my_cursor.execute(f"SELECT EXISTS(SELECT * from my_notes_app WHERE id={self.global_id});")
        result = self.my_cursor.fetchone()
        if result[0] >= 1:
            updated_content_in_textarea = self.textarea.get(1.0, tk.END)
            self.my_cursor.execute(f"UPDATE my_notes_app SET notes_content=%s WHERE id={self.global_id};",
                              (updated_content_in_textarea,))
            self.db.commit()
            self.refresh_updated_data()
        else:
            messagebox.showinfo("Selected note not available",
                                "Please save as a new note since the note you selected is already deleted!")

    # Function to display all rows from the table 'my_notes_app' in a scrollable frame 'scrollable_frame'.
    # For every row fetched from the table, there will be a 'edit' button and 'delete' button.
    def refresh_updated_data(self):
        try:
            self.my_cursor.execute("SELECT * FROM my_notes_app;")
            # Delete all widgets inside the frame 'scrollable_frame'.
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            # Add new widgets to frame 'scrollable_frame' byb fetching data from the table.
            for record in self.my_cursor:
                user_data = record[1]
                ptr = 1
                indexpoint = 90
                while indexpoint < len(user_data):
                    user_data = user_data[0:indexpoint] + "\n" + user_data[indexpoint:]
                    ptr += 1
                    indexpoint = indexpoint * ptr
                # Create a frame to place the Label and Button widgets in it.
                innerFrame = tk.Frame(self.scrollable_frame, background="#3742fa")
                innerFrame.pack(padx=1)
                # Label widget containing user data from fetched from table
                tk.Label(innerFrame, text=user_data, bg="#9AECDB", font=("Arial", 12), width=76, padx=2).grid(row=0,
                                                                                                              column=0,
                                                                                                              pady=1,
                                                                                                              padx=2)
                # Button created to place next to the Label
                edit_button = tk.Button(innerFrame, text=record[0], image=self.edit_icon_image, bg="#2ed573", bd=0)
                edit_button.grid(row=0, column=1, padx=3)
                edit_button.bind("<Button-1>", self.edit_note_in_textarea)
                del_btn = tk.Button(innerFrame, text=record[0], image=self.delete_icon_image, bd=0, width=30, bg="#ff4757")
                del_btn.grid(row=0, column=2)
                del_btn.bind("<Button-1>", self.delete_selected_note_from_database)
                separator = ttk.Separator(innerFrame, orient='horizontal')
        except:
            messagebox.showerror("Error occurred", "Unable to refresh")


    # Function to delete all the notes saved in a single click.
    def delete_all_notes(self):
        try:
            if messagebox.askquestion("Delete All?",
                                      "Do you really want to delete all your notes?\nNotes once deleted cannot be recovered") == "yes":
                # Delete all frames inside the frame 'scrollable_frame'.
                for widget in self.scrollable_frame.winfo_children():
                    widget.destroy()
                # Execute the MySQL query to delete all rows from the table 'my_notes_app'.
                self.my_cursor.execute("DELETE FROM my_notes_app;")
                # Make sure to commit the changes to the database.
                self.db.commit()
                # Display the refreshed canvas.
                self.refresh_updated_data()
        except:
            messagebox.showerror("Error", "Unable to delete all notes from database")

    def show_about(self):
        messagebox.showinfo("About My Notes App","Version:1.0.0\nDate of release:17th June 2024\nCopyright: 2024 Reshma Haridhas. All Rights Reserved")