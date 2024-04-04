from tkinter import Tk, Label, LabelFrame, Frame, Entry, Button, messagebox
import mysql.connector

class Admin_App:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#000000")
        self.root.title("Billing System")
        title = Label(self.root, text="Water Billing System Admin Panel", bd=15, relief="ridge", font=("Arial Black", 20),
                      bg="#000000", fg="white")
        title.pack(fill="x")

        # MySQL connection
        self.connection = mysql.connector.connect(host="localhost", user="root", password="", database="waterbillingsystem")
        self.cursor = self.connection.cursor()

        # Add Staff account label frame
        details = LabelFrame(self.root, text="Add Staff account", font=("Arial Black", 15), bg="#444444", fg="white",
                             relief="groove", bd=10)
        details.place(x=0, y=80, relwidth=1, height=170)

        staff_firstname_label = Label(details, text="First Name", font=("Arial Black", 12), bg="#000000", fg="white")
        staff_firstname_label.grid(row=0, column=0, padx=15)
        self.staff_firstname_entry = Entry(details, borderwidth=5, width=50)
        self.staff_firstname_entry.grid(row=0, column=1, padx=8)

        staff_lastname_label = Label(details, text="Last Name", font=("Arial Black", 12), bg="#000000", fg="white")
        staff_lastname_label.grid(row=0, column=2, padx=10)
        self.staff_lastname_entry = Entry(details, borderwidth=5, width=50)
        self.staff_lastname_entry.grid(row=0, column=3, padx=8)

        staff_username_label = Label(details, text="Username", font=("Arial Black", 12), bg="#000000", fg="white")
        staff_username_label.grid(row=3, column=2, padx=10)
        self.staff_username_entry = Entry(details, borderwidth=5, width=50)
        self.staff_username_entry.grid(row=3, column=3, padx=8)
        
        staff_password_label = Label(details, text="Password", font=("Arial Black", 12), bg="#000000", fg="white")
        staff_password_label.grid(row=0, column=4, padx=10)
        self.staff_password_entry = Entry(details, borderwidth=5, width=50)
        self.staff_password_entry.grid(row=0, column=5, padx=8)

        staff_contact_label = Label(details, text="Contact no.", font=("Arial Black", 12), bg="#000000", fg="white")
        staff_contact_label.grid(row=3, column=0, padx=10)
        self.staff_contact_entry = Entry(details, borderwidth=5, width=50)
        self.staff_contact_entry.grid(row=3, column=1, padx=8)

        button_frame = Frame(details, relief="groove", bg="#444444")
        button_frame.place(x=1200, y=60, width=200, height=70)

        button_add_account = Button(button_frame, text="Add Account", font=("Arial Black", 15), pady=5, bg="#444444",fg="#ffffff", command=self.register)
        button_add_account.grid(row=0, column=0, padx=12)

        # Staff list label frame
        View = LabelFrame(self.root, bg="#444444", fg="#ffffff", relief="groove", bd=10)
        View.place(x=0, y=250, height=435, width=1535)
        Views = LabelFrame(self.root, text="Staff list", font=("Arial Black", 12), bg="#000000", fg="#ffffff")
        Views.place(x=15, y=265, height=398, width=1505)
        self.view_staff_list(Views)

        # Admin menu
        billing_menu=LabelFrame(self.root,text="Options",font=("Arial Black",20),relief="groove",bd=10,bg="#444444",fg="white")
        billing_menu.place(x=0,y=690,relwidth=1,height=170)
        
        button_frame=Frame(billing_menu,bd=7,relief="groove",bg="#000000")
        button_frame.place(x=740,width=660,height=95)
        
        button_total=Button(button_frame,text="Bill history",font=("Arial Black",15),pady=10,bg="#444444",fg="#ffffff",command=lambda:self.total()).grid(row=0,column=0,padx=12)
        button_clear=Button(button_frame,text="Customer list",font=("Arial Black",15),pady=10,bg="#444444",fg="#ffffff",command=lambda:self.clear()).grid(row=0,column=1,padx=10,pady=6)
        button_exit=Button(button_frame,text="Dashboard",font=("Arial Black",15),pady=10,bg="#444444",fg="#ffffff",width=8,command=lambda:self.exit1()).grid(row=0,column=2,padx=10,pady=6)
        button_exit=Button(button_frame,text="Sign out",font=("Arial Black",15),pady=10,bg="#444444",fg="#ffffff",width=8,command=lambda:self.exit1()).grid(row=0,column=3,padx=10,pady=6)

    def register(self):
        firstname = self.staff_firstname_entry.get().strip()
        lastname = self.staff_lastname_entry.get().strip()
        username = self.staff_username_entry.get().strip()
        password = self.staff_password_entry.get().strip()
        contact = self.staff_contact_entry.get().strip()

        if len(firstname) > 0 and len(lastname) > 0 and len(password) > 0 and len(contact) > 0:
            vals = (firstname, lastname, password, contact)
            insert_query = "INSERT INTO `staff`(`firstname`, `lastname`, `username`, `password`, `contact`) VALUES (%s,%s,%s,%s,%s)"
            self.cursor.execute(insert_query, vals)
            self.connection.commit()
            messagebox.showinfo('Register', 'Your account has been created successfully')
            self.clear_entries()
            self.view_staff_list()
        else:
            messagebox.showwarning('Empty Fields', 'Make sure to enter all the information')

    def view_staff_list(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        query = "SELECT * FROM staff"
        self.cursor.execute(query)
        staff_list = self.cursor.fetchall()

        # Header labels
        header_labels = ["ID", "First Name", "Last Name", "Username", "Password", "Contact", "Actions"]
        for col, header in enumerate(header_labels):
            header_label = Label(frame, text=header, font=("Arial", 12, "bold"), bg="#444444", fg="#ffffff")
            header_label.grid(row=0, column=col, padx=25, pady=5, sticky="w")

        # Staff entries
        for index, staff in enumerate(staff_list, start=1):
            for col, info in enumerate(staff, start=0):
                label = Label(frame, text=info, font=("Arial", 12), bg="#000000", fg="#ffffff")
                label.grid(row=index, column=col, padx=25, pady=5, sticky="w")
            update_button = Button(frame, text="Update", font=("Arial", 10), bg="#007bff", fg="#ffffff", command=lambda idx=index: self.update_staff(staff_list[idx-1]))
            update_button.grid(row=index, column=len(staff_list[0]), padx=5, pady=5, sticky="w")
            delete_button = Button(frame, text="Delete", font=("Arial", 10), bg="#dc3545", fg="#ffffff", command=lambda idx=index: self.delete_staff(staff_list[idx-1][0]))
            delete_button.grid(row=index, column=len(staff_list[0]) + 1, padx=5, pady=5, sticky="w")

    def clear_entries(self):
        self.staff_firstname_entry.delete(0, "end")
        self.staff_lastname_entry.delete(0, "end")
        self.staff_password_entry.delete(0, "end")
        self.staff_contact_entry.delete(0, "end")

    def update_staff(self, staff_info):
        # Implementation for updating staff entry
        pass

    def delete_staff(self, staff_id):
        confirmation = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this staff entry?")
        if confirmation:
            delete_query = "DELETE FROM staff WHERE id = %s"
            self.cursor.execute(delete_query, (staff_id,))
            self.connection.commit()
            messagebox.showinfo("Success", "Staff entry deleted successfully.")
            self.view_staff_list()

    def exit(self):
        self.connection.close()
        self.root.destroy()

    def exit1(self):
        self.root.withdraw()
        

if __name__ == "__main__":
    root = Tk()
    obj = Admin_App(root)
    root.mainloop()

