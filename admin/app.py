import os
import sys
import pymongo
import smtplib
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

mongodb_entry = None
u_name = None



def mailsender(ssender_email, ssender_password, temail, ssubject, sbody):
    sender_email = ssender_email
    sender_password = ssender_password
    to_email = temail
    subject = ssubject
    body = sbody

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message.as_string())

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def firstpage():
    global mongodb_entry

    for widget in root.winfo_children():
        widget.destroy()

    first_frame = tk.Frame(root, bg="#f0f0f0")
    first_frame.pack(expand=True, fill="both")
    
    mongodb_label = tk.Label(first_frame, text="Enter MongoDB URI:", font=("Bahnschrift", 14, 'bold'))
    mongodb_label.pack(pady=(50, 5))
    mongodb_entry = tk.Entry(first_frame, font=("Bahnschrift", 14, 'bold'), bd=1, relief="groove")
    mongodb_entry.pack(pady=10)

    connect_button = tk.Button(first_frame, text="Connect to MongoDB", font=("Bahnschrift", 14, 'bold'), bg="#4E91FD", fg="white", command=connect_to_mongodb, width=20)
    connect_button.pack(pady=20)

    first_frame.place(relx=0.5, rely=0.5, anchor="center")

def check_credentials(username, password):
    global u_name
    u_name = username
    user = admin_collection.find_one({"_id": username, "password": password})
    return user is not None

def connect_to_mongodb():
    global client, db, admin_collection, doctor_collection, patient_collection, patient_login_collection, consultation_collection, doctor_login_collection, data_collection
    mongo_uri = mongodb_entry.get()
    try:
        client = pymongo.MongoClient(mongo_uri)
        db = client["Vaidhya"]
        admin_collection = db["admin"]
        doctor_collection = db["doctor_info"]
        patient_collection = db["patient_info"]
        patient_login_collection = db["patient_login"]
        consultation_collection = db["consultation"]
        doctor_login_collection = db["doctor_login"]
        data_collection = db["data"]
        messagebox.showinfo("MongoDB Connection", "Connected successfully!")
        show_login_screen()
    except pymongo.errors.ConnectionFailure:
        messagebox.showerror("MongoDB Connection Error", "Failed to connect to MongoDB")

def disconnect_from_mongodb():
    global client
    if client:
        client.close()
        messagebox.showinfo("MongoDB Disconnection", "Disconnected successfully!")
        firstpage()
    else:
        messagebox.showinfo("MongoDB Disconnection", "Already disconnected")


def show_login_screen():
    for widget in root.winfo_children():
        widget.destroy() 

    title_bar = tk.Frame(root, relief=tk.SUNKEN)
    title_bar.pack(side=tk.TOP, fill=tk.X)

    login_frame = tk.Frame(root, bg="#f0f0f0")
    login_frame.pack(expand=True, fill="both")

    disconnect_button = tk.Button(title_bar, text="Disconnect", command=disconnect_from_mongodb, font=("Bahnschrift", 10, 'bold'), fg="black", width=10)
    disconnect_button.pack(side=tk.RIGHT, padx=25, pady=25)

    label_username = tk.Label(login_frame, text="Username", font=("Bahnschrift", 14, 'bold'), bg="#f0f0f0")
    label_username.pack(pady=(50, 5))

    entry_username = tk.Entry(login_frame, font=("Bahnschrift", 14, 'bold'), bd=1, relief="groove")
    entry_username.pack(pady=10, padx=20)

    label_password = tk.Label(login_frame, text="Password", font=("Bahnschrift", 14, 'bold'), bg="#f0f0f0")
    label_password.pack(pady=(30, 5))

    entry_password = tk.Entry(login_frame, show="*", font=("Bahnschrift", 14, 'bold'), bd=1, relief="groove")
    entry_password.pack(pady=10, padx=20)

    def login():
        username = entry_username.get()
        password = entry_password.get()
        
        if check_credentials(username, password):
            messagebox.showinfo("Login", "Login successful!")
            show_main_menu()
        else:
            messagebox.showerror("Login", "Invalid username or password")

    button_login = tk.Button(login_frame, text="Login", font=("Bahnschrift", 14, 'bold'), bg="#4E91FD", fg="white", command=login, width=18)
    button_login.pack(pady=60)

    login_frame.place(relx=0.5, rely=0.5, anchor="center")



def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()  

    title_bar = tk.Frame(root, relief=tk.SUNKEN)
    title_bar.pack(side=tk.TOP, fill=tk.X)

    B_frame = tk.Frame(root, bg="#f0f0f0")
    B_frame.pack(expand=True, fill="both")

    button_logout = tk.Button(title_bar, text="Logout", font=("Bahnschrift", 10, 'bold'), fg="black", width=10, command=show_login_screen)
    button_logout.pack(side=tk.RIGHT, padx=25, pady=25)

    button_mapping = tk.Button(B_frame, text="Doctor-Patient Mapping", command=doctor_patient_mapping, font=("Bahnschrift", 14, 'bold'), bg="#FF7F3E", fg="white", width=19)
    button_mapping.pack(pady=20)

    button_delete_doctor = tk.Button(B_frame, text="Delete Doctor Account", command=delete_doctor_account, font=("Bahnschrift", 14, 'bold'), bg="#9DDE8B", fg="white", width=18)
    button_delete_doctor.pack(pady=20)

    button_delete_patient = tk.Button(B_frame, text="Delete Patient Account", command=delete_patient_account, font=("Bahnschrift", 14, 'bold'), bg="#AD88C6", fg="white", width=18)
    button_delete_patient.pack(pady=20)

    B_frame.place(relx=0.5, rely=0.5, anchor="center")

def doctor_patient_mapping():
    for widget in root.winfo_children():
        widget.destroy()  

    title_bar = tk.Frame(root, relief=tk.SUNKEN)
    title_bar.pack(side=tk.TOP, fill=tk.X)

    C_frame = tk.Frame(root, bg="#f0f0f0")
    C_frame.pack(expand=True, fill="both")

    button_back = tk.Button(title_bar, text="Back", command=show_main_menu, font=("Bahnschrift", 10, 'bold'), fg="black", width=10)
    button_back.pack(side=tk.RIGHT, padx=25, pady=25)

    doctor_ids = [str(doc['_id']) for doc in doctor_collection.find()]
    patient_ids = [str(doc['_id']) for doc in patient_collection.find()]

    label_doctor = tk.Label(C_frame, text="Select Doctor ID", font=("Bahnschrift", 14, 'bold'), bg="#f0f0f0")
    label_doctor.pack(pady=10)
    combo_doctor = ttk.Combobox(C_frame, values=doctor_ids, font=("Bahnschrift", 14, 'bold'))
    combo_doctor.pack(pady=10)

    label_patient = tk.Label(C_frame, text="Select Patient ID", font=("Bahnschrift", 14, 'bold'), bg="#f0f0f0")
    label_patient.pack(pady=(30, 10))
    combo_patient = ttk.Combobox(C_frame, values=patient_ids, font=("Bahnschrift", 14, 'bold'))
    combo_patient.pack(pady=10)

    def submit_mapping():
        selected_doctor_id = combo_doctor.get()
        selected_patient_id = combo_patient.get()
        try:
        
            if selected_doctor_id and selected_patient_id:
                consultation_record = {
                    "_id": selected_patient_id,
                    "doctor_id": selected_doctor_id
                }
                consultation_collection.insert_one(consultation_record)
                doc = doctor_collection.find_one({"_id": selected_doctor_id})
                doctor_name = doc['doctor_name']
                key = selected_doctor_id + doctor_name[0:2]
                patient = patient_collection.find_one({"_id": selected_patient_id})
                patient_username = patient['patient_username']
                query = data_collection.find_one({"_id": patient_username})

                new_query = {
                    "$set" : {
                        "key": key,
                        "doctor_name":doctor_name,
                        "doctor_id": selected_doctor_id
                    }
                }
                data_collection.update_one(query, new_query)

                user = admin_collection.find_one({"_id": u_name})
                
                doc_email = doc['email']
                doc_name = doc['doctor_name']
                patient_email = patient['email']
                patient_name = patient['patient_name']

                sender_mail = user['email']
                sender_password = user['email_app_password']

                d_subject = "New Patient Assigned"
                d_body = f"Dear {doc_name},\n\nThank you for registering with Vaidhya.\nYou Have been Assigned a new Patient.\n\nPatient Details:\nPatient Name: {patient_name}\nPatient ID: {patient['_id']}\nPatient Email: {patient_email}\nPatient Contact: {patient['ph_number']}\n\nThank you for your cooperation, we greatly advise you to contact your Patient as soon as possible.\n\nThanks & Regards,\nVaidhya"            

                p_subject = "New Doctor Assigned"
                p_body = f"Dear {patient_name},\n\nThank you for registering with Vaidhya.\nYou Have been Assigned a new Doctor.\n\nDoctor Details:\nDoctor Name: {doc_name}\nDoctor Email: {doc_email}\nDoctor Contact: {doc['ph_number']}\n\nThank you for your cooperation, we greatly advise you to contact your Doctor as soon as possible.\n\nThanks & Regards,\nVaidhya"            

                mailsender(sender_mail, sender_password, doc_email, d_subject, d_body)
                mailsender(sender_mail, sender_password, patient_email, p_subject, p_body)
                messagebox.showinfo("Success", "Consultation record saved successfully")
            else:
                messagebox.showerror("Error", "Please select both doctor and patient IDs")
        except:
            messagebox.showerror("Error", "Something Went Wrong!!")

    button_submit = tk.Button(C_frame, text="Submit", command=submit_mapping, font=("Bahnschrift", 14, 'bold'), bg="#C73659", fg="white",width=18)
    button_submit.pack(pady=40)

    C_frame.place(relx=0.5, rely=0.5, anchor="center")

def delete_doctor_account():
    for widget in root.winfo_children():
        widget.destroy()  

    title_bar = tk.Frame(root, relief=tk.SUNKEN)
    title_bar.pack(side=tk.TOP, fill=tk.X)

    D_frame = tk.Frame(root, bg="#f0f0f0")
    D_frame.pack(expand=True, fill="both")

   
    button_back = tk.Button(title_bar, text="Back", command=show_main_menu, font=("Bahnschrift", 10, 'bold'), fg="black", width=10)
    button_back.pack(side=tk.RIGHT, padx=25, pady=25)

    label_doctor_id = tk.Label(D_frame, text="Enter Doctor ID",  font=("Bahnschrift", 14, 'bold'), bg="#f0f0f0")
    label_doctor_id.pack(pady=10)
    entry_doctor_id = tk.Entry(D_frame, font=("Bahnschrift", 14, 'bold'))
    entry_doctor_id.pack(pady=10)

    def submit_delete():
        doctor_id = entry_doctor_id.get()

        try:
        
            if doctor_id:
                doctor_record = doctor_collection.find_one({"_id": doctor_id})
                if doctor_record:
                    doctor_username = doctor_record.get("doctor_username")
                    if doctor_username:
                        doctor_collection.delete_one({"_id": doctor_id})
                        doctor_login_collection.delete_one({"_id": doctor_username})
                        user = admin_collection.find_one({"_id": u_name})
                        doctor_mail_id = doctor_record['email']
                        doctor_name = doctor_record['doctor_name']
                        sender_mail = user['email']
                        sender_password = user['email_app_password']
                        subject = "Account Deletion Request"
                        message = f"Dear {doctor_name},\n\nYour Vaidhya Doctor Account with Doctor ID {doctor_id} and associated login {doctor_username} has been deleted successfully.\n\nThanks and Regards,\nVaidhya."
                        mailsender(sender_mail, sender_password, doctor_mail_id, subject, message)
                        messagebox.showinfo("Success", f"Doctor ID {doctor_id} and associated login {doctor_username} deleted successfully")
                    else:
                        messagebox.showerror("Error", "Doctor username not found")
                else:
                    messagebox.showerror("Error", "Doctor ID not found")
            else:
                messagebox.showerror("Error", "Please enter a Doctor ID")
        except:
            messagebox.showerror("Error", "Something Went Wrong!!")


    button_submit = tk.Button(D_frame, text="Submit", command=submit_delete,  font=("Bahnschrift", 14, 'bold'), bg="#C73659", fg="white",width=18)
    button_submit.pack(pady=20)

    D_frame.place(relx=0.5, rely=0.5, anchor="center")

def delete_patient_account():
    for widget in root.winfo_children():
        widget.destroy()  

    title_bar = tk.Frame(root, relief=tk.SUNKEN)
    title_bar.pack(side=tk.TOP, fill=tk.X)

    E_frame = tk.Frame(root, bg="#f0f0f0")
    E_frame.pack(expand=True, fill="both")

    button_back = tk.Button(title_bar, text="Back", command=show_main_menu, font=("Bahnschrift", 10, 'bold'), fg="black", width=10)
    button_back.pack(side=tk.RIGHT, padx=25, pady=25)

    label_patient_id = tk.Label(E_frame, text="Enter Patient ID", font=("Bahnschrift", 14, 'bold'), bg="#f0f0f0")
    label_patient_id.pack(pady=10)
    entry_patient_id = tk.Entry(E_frame,font=("Bahnschrift", 14, 'bold'))
    entry_patient_id.pack(pady=10)

    def submit_delete_patient():
        patient_id = entry_patient_id.get()
        try:
            if patient_id:
                patient_record = patient_collection.find_one({"_id": patient_id})
                if patient_record:
                    patient_username = patient_record.get("patient_username")
                    if patient_username:
                        patient_collection.delete_one({"_id": patient_id})
                        patient_login_collection.delete_one({"_id": patient_username})
                        data_collection.delete_one({"_id": patient_username})

                        user = admin_collection.find_one({"_id": u_name})
                        patient_mail_id = patient_record['email']
                        patient_name = patient_record['patient_name']
                        sender_mail = user['email']
                        sender_password = user['email_app_password']
                        subject = "Account Deletion Request"
                        message = f"Dear {patient_name},\n\nYour Vaidhya Patient Account with Patient ID {patient_id} and associated login {patient_username} has been deleted successfully.\n\nThanks and Regards,\nVaidhya."
                        mailsender(sender_mail, sender_password, patient_mail_id, subject, message)

                        messagebox.showinfo("Success", f"Patient ID {patient_id} and associated login {patient_username} deleted successfully")
                    else:
                        messagebox.showerror("Error", "Patient username not found")
                else:
                    messagebox.showerror("Error", "Patient ID not found")
            else:
                messagebox.showerror("Error", "Please enter a Patient ID")
        except:
            messagebox.showerror("Error", "Something Went Wrong!!")

    button_submit = tk.Button(E_frame, text="Submit", command=submit_delete_patient, font=("Bahnschrift", 14, 'bold'), bg="#C73659", fg="white",width=18)
    button_submit.pack(pady=40)

    E_frame.place(relx=0.5, rely=0.5, anchor="center")

root = tk.Tk()
root.title("Vaidhya")

root.iconbitmap(resource_path('assets\\logo.ico'))

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = screen_width // 2
window_height = screen_height * 2 // 3
window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 3

root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

firstpage()

root.mainloop()