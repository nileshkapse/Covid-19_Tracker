from tkinter import *
from tkinter import ttk
from tkcalendar import *
from state_and_cities import *
from tkinter import messagebox
import mysql.connector

# Make connection to database
cnx = mysql.connector.connect(user="username",
                              password="password",
                              host="host",
                              database="database_name")

# Create cursor object
cursor = cnx.cursor(buffered=True)

# Check that connection created successfully or not
if cnx:
    print("cnxection Successful :)")
else:
    print("cnxection Failed :")


# Government Class
class Government:
    isLogin = False

    government_details = {
        "state_id": '',
        "name": '',
        "state": '',
        "patient_capacity": 0,
        "patient_count": 0,
        "patient_admitted_count": 0,
        "ventilators_count": 0,
    }

    @staticmethod
    def set_government_details(state_id, name, state, password, patient_capacity, patient_count, patient_admitted_count,
                               ventilators_count, ):
        try:
            # Updating government_details dictionary
            Government.government_details['state_id'] = state_id
            Government.government_details['name'] = name
            Government.government_details['state'] = state
            Government.government_details['password'] = password
            Government.government_details['patient_capacity'] = patient_capacity
            Government.government_details['patient_count'] = patient_count
            Government.government_details['patient_admitted_count'] = patient_admitted_count
            Government.government_details['ventilators_count'] = ventilators_count

        except KeyError as key_e:
            print("Error: ", key_e)
        except Exception as key_exc:
            print("Exception: ", key_exc)


# Hospital Class
class Hospital:
    isLogin = False
    isPositiveDateChanged = False
    isNegativeDateChanged = False
    isAdmittedDateChanged = False
    isDischargeDateChanged = False
    isDeadDateChanged = False

    hospital_details = {
        "id": "",
        "name": "",
        "patient_capacity": 0,
        "patient_count": 0,
        "patient_admitted_count": 0,
        "ventilators_count": 0,
        "address": "",
        "city": "",
        "state": "",
        "state_id": "",
        "password": "password"
    }

    @staticmethod
    def set_hospital_details(hospital_id, hospital_name, patient_capacity, total_patient_count,
                             total_patient_admitted_count, total_ventilators, address, city, state, state_id, password):
        try:

            # Updating hospital_details dictionary
            Hospital.hospital_details['id'] = hospital_id
            Hospital.hospital_details['name'] = hospital_name
            Hospital.hospital_details['patient_capacity'] = patient_capacity
            Hospital.hospital_details['patient_count'] = total_patient_count
            Hospital.hospital_details['patient_admitted_count'] = total_patient_admitted_count
            Hospital.hospital_details['ventilators_count'] = total_ventilators
            Hospital.hospital_details['address'] = address
            Hospital.hospital_details['city'] = city
            Hospital.hospital_details['state'] = state
            Hospital.hospital_details['state_id'] = state_id
            Hospital.hospital_details['password'] = password

        except KeyError as key_e:
            print("Error: ", key_e)
        except Exception as key_exc:
            print("Exception: ", key_exc)

    @staticmethod
    def set_hospital_update_details(patient_capacity, total_ventilators, address):
        try:

            # Updating hospital_details dictionary
            '''
            Hospital.hospital_details['id'] = hospital_id
            Hospital.hospital_details['name'] = hospital_name
            '''
            Hospital.hospital_details['patient_capacity'] = patient_capacity
            '''
            Hospital.hospital_details['patient_count'] = total_patient_count
            Hospital.hospital_details['patient_admitted_count'] = total_patient_admitted_count
            '''
            Hospital.hospital_details['ventilators_count'] = total_ventilators
            Hospital.hospital_details['address'] = address
            '''Hospital.hospital_details['city'] = city
            Hospital.hospital_details['state'] = state
            Hospital.hospital_details['state_id'] = state_id'''
        except KeyError as key_e:
            print("Error: ", key_e)
        except Exception as key_exc:
            print("Exception: ", key_exc)

    @staticmethod
    def positive_date_changed(e):
        Hospital.isPositiveDateChanged = True
        print("Positive Date Changed")

    @staticmethod
    def negative_date_changed(e):
        Hospital.isNegativeDateChanged = True
        print("Negative Date Changed")

    @staticmethod
    def admitted_date_changed(e):
        Hospital.isAdmittedDateChanged = True
        print("Admitted Date Changed")

    @staticmethod
    def discharge_date_changed(e):
        Hospital.isDischargeDateChanged = True
        print("Discharge Date Changed")

    @staticmethod
    def dead_date_changed(e):
        Hospital.isDeadDateChanged = True
        print("Dead Date Changed")


# Creating main window
root = Tk()
root.geometry("800x600-280-80")
root.resizable(False, False)
root.title("Covid19 Tracker")

'''
Common Functions
'''


# function to show and hide frame
def show_and_destroy_frame(frame_to_show, frame_to_hide):
    frame_to_show()
    frame_to_hide.destroy()


# function to display header
def display_header(header_name, button_name, button_color, header_name_spacing, current_frame, next_frame):
    header = Frame(current_frame, bg="#0000ff", height=53)
    header.pack_propagate(0)

    header_contents = Frame(header, height=50, pady=10, bg="#e9e9e9")
    header_contents.pack_propagate(0)

    Button(header_contents, text=button_name, bd=0, bg=button_color, fg="#ffffff",
           width=10, height=3, font=("calibri", 12),
           command=lambda: show_and_destroy_frame(next_frame, current_frame)). \
        pack(side=LEFT, padx=20)

    Label(header_contents, text=header_name, font=("calibri", 16, "bold"), bg="#e9e9e9"). \
        pack(side=LEFT, padx=header_name_spacing)

    header_contents.pack(fill=X)

    header.pack(fill=X)


# function to display patients data
def display_patients():
    global hospital_display_patients_frame

    hospital_display_patients_frame = Frame(root, width=800, height=600)
    hospital_display_patients_frame.pack_propagate(0)

    if Government.isLogin:
        display_header("Government Display Patients", "Back", "#00A439", 155, hospital_display_patients_frame,
                       government_dashboard)
    else:
        display_header("Hospital Display Patients", "Back", "#00A439", 155, hospital_display_patients_frame,
                       hospital_dashboard)

    # Table Frame
    hospital_display_patients_table_frame = Frame(
        hospital_display_patients_frame, width=800)

    hospital_table = ttk.Treeview(hospital_display_patients_table_frame,
                                  columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16), show="headings",
                                  height=30, )

    vsb = ttk.Scrollbar(hospital_display_patients_table_frame,
                        orient="vertical", command=hospital_table.yview)
    vsb.pack(side=RIGHT, fill=Y)

    hsb = ttk.Scrollbar(hospital_display_patients_table_frame,
                        orient="horizontal", command=hospital_table.xview)
    hsb.pack(side=BOTTOM, fill=X)

    hospital_table.configure(yscrollcommand=vsb.set)
    hospital_table.configure(xscrollcommand=hsb.set)

    hospital_table.column("1", width=50)
    hospital_table.column("2", width=100)
    hospital_table.column("3", width=180)
    hospital_table.column("4", width=50)
    hospital_table.column("5", width=180)
    hospital_table.column("6", width=100)
    hospital_table.column("7", width=100)
    hospital_table.column("8", width=80)
    hospital_table.column("9", width=80)
    hospital_table.column("10", width=80)
    hospital_table.column("11", width=120)
    hospital_table.column("12", width=100)
    hospital_table.column("13", width=100)
    hospital_table.column("14", width=100)
    hospital_table.column("15", width=100)
    hospital_table.column("16", width=100)

    hospital_table.heading("1", text="Sr.No")
    hospital_table.heading("2", text="Aadhar No")
    hospital_table.heading("3", text="Name")
    hospital_table.heading("4", text="Age")
    hospital_table.heading("5", text="Address")
    hospital_table.heading("6", text="Mobile No")
    hospital_table.heading("7", text="State")
    hospital_table.heading("8", text="City")
    hospital_table.heading("9", text="Country")
    hospital_table.heading("10", text="Covid Status")
    hospital_table.heading("11", text="Quarantine Type")
    hospital_table.heading("12", text="Positive Date")
    hospital_table.heading("13", text="Negative Date")
    hospital_table.heading("14", text="Admitted Date")
    hospital_table.heading("15", text="Discharge Date")
    hospital_table.heading("16", text="Dead Date")

    records = []
    try:
        if Government.isLogin:
            if Government.government_details['state_id'] == "admin":
                query = "SELECT aadhar_no, full_name, age, address, mob_no, state, city, country, covid_status," \
                        " quarantine_type, positive_date, negative_date, admitted_date, discharge_date, dead_date " \
                        "FROM patient;"
                cursor.execute(query)
            else:
                query = 'SELECT aadhar_no, full_name, age, address, mob_no, state, city, country, covid_status, ' \
                        'quarantine_type, positive_date, negative_date, admitted_date, discharge_date, dead_date ' \
                        'FROM patient WHERE state_id = \"' + str(Government.government_details['state_id']) + '\";'
                cursor.execute(query)

            records = cursor.fetchall()
            print(records)
        elif Hospital.isLogin:
            query = 'SELECT aadhar_no, full_name, age, address, mob_no, state, city, country, covid_status, ' \
                    'quarantine_type, positive_date, negative_date, admitted_date, discharge_date, dead_date' \
                    ' FROM patient WHERE hospital_id = \"' + str(Hospital.hospital_details['id']) + '\";'
            cursor.execute(query)
            records = cursor.fetchall()
            print(records)
    except mysql.connector.Error as err:
        print(err)
    except Exception as e:
        print(e)

    i = 1
    for item in records:
        columns_heading = ["" + str(i)] + list(item)
        hospital_table.insert('', 'end', values=columns_heading)
        i = i + 1

    hospital_table.pack(side=LEFT, fill=X, expand=True)

    hospital_display_patients_table_frame.pack()

    hospital_display_patients_frame.pack()


# function to display hospitals data
def display_hospitals():
    global government_display_hospitals_frame

    government_display_hospitals_frame = Frame(root, width=800, height=600)
    government_display_hospitals_frame.pack_propagate(0)

    display_header("Government Display Hospitals", "Back", "#00A439", 155, government_display_hospitals_frame,
                   government_dashboard)

    # Table Frame
    government_display_hospitals_table_frame = Frame(
        government_display_hospitals_frame, width=800)

    government_hospital_table = ttk.Treeview(government_display_hospitals_table_frame,
                                             columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13),
                                             show="headings",
                                             height=30, )

    vsb = ttk.Scrollbar(government_display_hospitals_table_frame,
                        orient="vertical", command=government_hospital_table.yview)
    vsb.pack(side=RIGHT, fill=Y)

    hsb = ttk.Scrollbar(government_display_hospitals_table_frame,
                        orient="horizontal", command=government_hospital_table.xview)
    hsb.pack(side=BOTTOM, fill=X)

    government_hospital_table.configure(yscrollcommand=vsb.set)
    government_hospital_table.configure(xscrollcommand=hsb.set)

    government_hospital_table.column("1", width=50)
    government_hospital_table.column("2", width=100)
    government_hospital_table.column("3", width=180)
    government_hospital_table.column("4", width=50)
    government_hospital_table.column("5", width=180)
    government_hospital_table.column("6", width=100)
    government_hospital_table.column("7", width=100)
    government_hospital_table.column("8", width=80)
    government_hospital_table.column("9", width=80)
    government_hospital_table.column("10", width=80)
    government_hospital_table.column("11", width=120)
    government_hospital_table.column("12", width=100)
    government_hospital_table.column("13", width=100)

    government_hospital_table.heading("1", text="Sr.No")
    government_hospital_table.heading("2", text="Hospital Id")
    government_hospital_table.heading("3", text="Name")
    government_hospital_table.heading("4", text="Address")
    government_hospital_table.heading("5", text="City")
    government_hospital_table.heading("6", text="State")
    government_hospital_table.heading("7", text="Patient Capacity")
    government_hospital_table.heading("8", text="Admitted Count")
    government_hospital_table.heading("9", text="Home Quarantine Count")
    government_hospital_table.heading("10", text="Ventilators Count")
    government_hospital_table.heading("11", text="Positive Count")
    government_hospital_table.heading("12", text="Negative Count")
    government_hospital_table.heading("13", text="Dead Count")

    records = []
    try:
        if Government.government_details['state_id'] == "admin":
            query = "SELECT hospital_id, hospital_name, address, city, state, patient_capacity, " \
                    "total_patient_admitted_count, home_quarantine_count, total_ventilators, positive_count, " \
                    "negative_count, dead_count FROM hospitals;"
            cursor.execute(query)
        else:
            query = "SELECT hospital_id, hospital_name, address, city, state, patient_capacity, " \
                    "total_patient_admitted_count, home_quarantine_count, total_ventilators, positive_count, " \
                    "negative_count, dead_count FROM hospitals where " \
                    "state_id=\"" + str(Government.government_details['state_id']) + "\";"
            cursor.execute(query)

        records = cursor.fetchall()
        print(records)

    except mysql.connector.Error as err:
        print(err)
    except Exception as e:
        print(e)

    i = 1
    for item in records:
        columns_heading = ["" + str(i)] + list(item)
        government_hospital_table.insert('', 'end', values=columns_heading)
        i = i + 1

    government_hospital_table.pack(side=LEFT, fill=X, expand=True)

    government_display_hospitals_table_frame.pack()

    government_display_hospitals_frame.pack()


# function to display governments data
def display_governments():
    global government_display_government_frame

    government_display_government_frame = Frame(root, width=800, height=600)
    government_display_government_frame.pack_propagate(0)

    display_header("Government Display Governments", "Back", "#00A439", 155, government_display_government_frame,
                   government_dashboard)

    # Table Frame
    government_display_hospitals_table_frame = Frame(
        government_display_government_frame, width=800)

    government_hospital_table = ttk.Treeview(government_display_hospitals_table_frame,
                                             columns=(1, 2, 3, 4),
                                             show="headings",
                                             height=30, )

    vsb = ttk.Scrollbar(government_display_hospitals_table_frame,
                        orient="vertical", command=government_hospital_table.yview)
    vsb.pack(side=RIGHT, fill=Y)

    hsb = ttk.Scrollbar(government_display_hospitals_table_frame,
                        orient="horizontal", command=government_hospital_table.xview)
    hsb.pack(side=BOTTOM, fill=X)

    government_hospital_table.configure(yscrollcommand=vsb.set)
    government_hospital_table.configure(xscrollcommand=hsb.set)

    government_hospital_table.column("1", width=100)
    government_hospital_table.column("2", width=250)
    government_hospital_table.column("3", width=250)
    government_hospital_table.column("4", width=250)

    government_hospital_table.heading("1", text="Sr.No")
    government_hospital_table.heading("2", text="State Id")
    government_hospital_table.heading("3", text="State Name")
    government_hospital_table.heading("4", text="Government Name")

    records = []
    try:

        query = "SELECT state_id, state_name, government_name FROM government where state_id != 'admin';"
        cursor.execute(query)

        records = cursor.fetchall()
        print(records)

    except mysql.connector.Error as err:
        print(err)
    except Exception as e:
        print(e)

    i = 1
    for item in records:
        columns_heading = ["" + str(i)] + list(item)
        government_hospital_table.insert('', 'end', values=columns_heading)
        i = i + 1

    government_hospital_table.pack(side=LEFT, fill=X, expand=True)

    government_display_hospitals_table_frame.pack()

    government_display_government_frame.pack()


'''
-------------------------------------------------------------------------------------------------------
                                        WELCOME FRAMES
-------------------------------------------------------------------------------------------------------
'''


# function to create homepage frame
def homepage():
    global homepage_frame
    global homepage_sub_frame1
    global canvas
    global img

    homepage_frame = Frame(root, width=800, height=600)
    homepage_frame.pack_propagate(0)

    # homepage sub-frame1
    homepage_sub_frame1 = Frame(homepage_frame, width=450, height=600)
    canvas = Canvas(homepage_sub_frame1, width=450, height=600)
    canvas.pack(fill=Y, expand=True)

    img = PhotoImage(file="./homepage_image.png")
    canvas.create_image(0, 0, anchor=NW, image=img)

    homepage_sub_frame2 = Frame(homepage_frame, width=350, height=600)

    homepage_title1 = Label(homepage_sub_frame2,
                            text="Welcome to", font=('Calibri', 35))
    homepage_title2 = Label(homepage_sub_frame2,
                            text="Covid19 Tracker", font=('Calibri', 35))
    homepage_info = Label(homepage_sub_frame2,
                          text="Python application that performs digital tracking of covid19 patients "
                               "to follow-up on their health status and enables hospitals and governments"
                               " to effectively and efficiently keep track of patients.",
                          font=('Calibri', 16), height=9, wraplength=240, justify=LEFT)
    homepage_button1 = Button(homepage_sub_frame2, text="Get Started..!",
                              command=lambda: show_and_destroy_frame(main_options, homepage_frame),
                              width=22, height=2, bg="#0000A0", fg="#ffffff", font=('calibri', 14), bd=1)

    homepage_title1.pack(padx=15)
    homepage_title2.pack(pady=15, padx=15)
    homepage_info.pack(pady=15, padx=15)
    homepage_button1.pack(pady=25, padx=15)

    homepage_sub_frame1.pack(side=LEFT)
    homepage_sub_frame2.pack(side=RIGHT)

    homepage_frame.pack()


# function to create main options frame
def main_options():
    global main_options_frame
    global main_options_container_1
    global main_options_container_2
    global main_options_image_frame
    global main_options_canvas
    global main_options_img

    # Main Options Frame
    main_options_frame = Frame(root, width=800, height=600)
    main_options_frame.pack_propagate(0)

    print("Government: ", Government.government_details)
    print("\ngovernmentIsLogin: ", Government.isLogin)
    print("Hospital: ", Hospital.hospital_details)
    print("\nhospitalIsLogin: ", Hospital.isLogin)

    display_header("Dashboard", "Back", "#00A439", 225,
                   main_options_frame, homepage)

    main_options_image_frame = Frame(
        main_options_frame, width=800, height=200, bg="#000000")
    main_options_canvas = Canvas(
        main_options_image_frame, width=800, height=200)
    main_options_canvas.pack(fill=X, expand=True)

    main_options_img = PhotoImage(file="./homepage_image.png")
    main_options_canvas.create_image(0, 0, anchor=NW, image=main_options_img)

    main_options_image_frame.pack()

    options_container = Frame(main_options_frame)

    # Options
    main_options_container_1 = Frame(options_container)
    main_options_container_2 = Frame(options_container)

    Button(main_options_container_1, text="Governments", width=20, height=4, bg="#FEAD00", fg="#ffffff", bd=1,
           relief="groove", font=("calibri", 17, "bold"),
           command=lambda: show_and_destroy_frame(government_signin, main_options_frame)).pack(padx=10, pady=10,
                                                                                               side=LEFT)
    Button(main_options_container_1, text="Hospitals", width=20, height=4, bg="#1DC100", fg="#ffffff", bd=1,
           relief="groove", font=("calibri", 17, "bold"),
           command=lambda: show_and_destroy_frame(hospital_signin, main_options_frame)).pack(padx=10, pady=10,
                                                                                             side=LEFT)

    Button(main_options_container_2, text="Public", width=20, height=4, bg="#00BBC1", fg="#ffffff", bd=1,
           relief="groove", font=("calibri", 17, "bold"),
           command=lambda: show_and_destroy_frame(public, main_options_frame)).pack(padx=10, pady=10, side=LEFT)
    # Button(main_options_container_2, text="Back", width=20, height=4, bg="#8800ED", fg="#ffffff", bd=1,
    #        relief="groove", font=("calibri", 17, "bold"),
    #        command=lambda: show_and_hide_frame(homepage_frame, main_options_frame)).pack(padx=10, pady=10, side=LEFT)

    main_options_container_1.pack(pady=(20, 0))
    main_options_container_2.pack()

    options_container.pack()

    main_options_frame.pack()


'''
-------------------------------------------------------------------------------------------------------
                                        GOVERNMENT SECTION
-------------------------------------------------------------------------------------------------------
'''

'''
handle_frame_operations
'''


# function to handle government signin
def handle_government_signin():
    global username
    username = government_username_entry.get()
    password = government_password_entry.get()
    # government_username_entry.delete(0, 'end')
    # government_password_entry.delete(0, 'end')
    # username = government_username_entry.get()
    # password = government_password_entry.get()
    if government_username_entry.get() == "" or government_password_entry.get() == "":
        messagebox.showerror("Error", "Both fields are required")
        government_username_entry.delete(0, 'end')
        government_password_entry.delete(0, 'end')

    else:
        try:
            query = "select * from government where state_id = %s and password = %s ;"
            data = (username, password)
            print(username)
            cursor.execute(query, data)
            row = cursor.fetchall()
            print(row)
            if len(row) == 0:
                messagebox.showerror("Error", "Invalid Username or Password")
                # government_username_entry.delete(0, 'end')
                # government_password_entry.delete(0, 'end')
                government_username_entry.delete(0, 'end')
                government_password_entry.delete(0, 'end')

            else:
                messagebox.showinfo("Information", "Welcome to Government dashboard")
                government_username_entry.delete(0, 'end')
                government_password_entry.delete(0, 'end')
                print(row)
                data_set = row[0]

                res1 = None
                res2 = None
                if data_set[0] != "admin":
                    query1 = "select sum(patient_capacity), sum(total_patient_admitted_count), sum(total_ventilators)" \
                             " from hospitals where state_id = \"" + data_set[0] + "\" GROUP BY state_id;"
                    cursor.execute(query1)
                    res1 = cursor.fetchall()

                    query2 = "select count(*) from patient where state_id = \"" + data_set[0] + "\";"
                    cursor.execute(query2)
                    res2 = cursor.fetchall()
                elif data_set[0] == "admin":
                    query1 = "select sum(patient_capacity), sum(total_patient_admitted_count), sum(total_ventilators)" \
                             " from hospitals;"
                    cursor.execute(query1)
                    res1 = cursor.fetchall()

                    query2 = "select count(*) from patient;"
                    cursor.execute(query2)
                    res2 = cursor.fetchall()

                if len(res2) == 0 and len(res1) == 0:
                    Government.set_government_details(data_set[0], data_set[3], data_set[2], data_set[1], 0,
                                                      0, 0, 0)
                elif len(res1) == 0:
                    Government.set_government_details(data_set[0], data_set[3], data_set[2], data_set[1], 0,
                                                      res2[0][0], 0, 0)
                elif len(res2) == 0:
                    Government.set_government_details(data_set[0], data_set[3], data_set[2], data_set[1], res1[0][0],
                                                      0, res1[0][1], res1[0][2])
                else:
                    Government.set_government_details(data_set[0], data_set[3], data_set[2], data_set[1], res1[0][0],
                                                      res2[0][0], res1[0][1], res1[0][2])

                Government.isLogin = True

                show_and_destroy_frame(government_dashboard, government_frame)

        except mysql.connector.Error as err:
            print("Exception: ", err)
        except ValueError:
            print("Please enter input correctly..!")
        except KeyboardInterrupt:
            print("Please do not try to interrupt execution of program..!")
        except EOFError:
            print("Please enter input..!")

    # print(username)
    # print(password)

    # show_and_hide_frame(government_dashboard_frame, government_frame)


# function to handle government logout
def handle_government_logout():
    # government logout
    # release memory
    Government.set_government_details("", "", "", "", 0, 0, 0, 0)
    Government.isLogin = False
    show_and_destroy_frame(main_options, government_dashboard_frame)


# function to change government password
def government_handle_change_password():
    old_password = change_password_old_password_entry1.get()
    new_password = change_password_new_password_entry1.get()
    repeated_new_password = change_password_repeated_new_password_entry1.get()

    if change_password_old_password_entry1.get() == "" or change_password_new_password_entry1.get() == "" or change_password_repeated_new_password_entry1.get() == "":
        messagebox.showerror("Error", "Fields are Empty")

        change_password_old_password_entry1.delete(0, 'end')
        change_password_new_password_entry1.delete(0, 'end')
        change_password_repeated_new_password_entry1.delete(0, 'end')


    elif new_password != repeated_new_password:
        messagebox.showerror("Error", "you enter different passwords ")

        change_password_old_password_entry1.delete(0, 'end')
        change_password_new_password_entry1.delete(0, 'end')
        change_password_repeated_new_password_entry1.delete(0, 'end')


    elif new_password == repeated_new_password:
        try:
            # password dictionary
            if old_password == (Government.government_details['password']):

                data = (new_password, Government.government_details['state_id'])
                query = "update government set password= %s where state_id=%s ;"
                cursor.execute(query, data)
                cnx.commit()
                row = cursor.fetchone()
                print(row)

                Government.government_details['password'] = new_password

                messagebox.showinfo("Information", "Password has been changed...")
                change_password_old_password_entry1.delete(0, 'end')
                change_password_new_password_entry1.delete(0, 'end')
                change_password_repeated_new_password_entry1.delete(0, 'end')
            else:
                messagebox.showerror("Error", "you Enter Wrong Old Password")
                change_password_old_password_entry1.delete(0, 'end')
                change_password_new_password_entry1.delete(0, 'end')
                change_password_repeated_new_password_entry1.delete(0, 'end')

        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Exception has been occur..")
            change_password_old_password_entry1.delete(0, 'end')
            change_password_new_password_entry1.delete(0, 'end')
            change_password_repeated_new_password_entry1.delete(0, 'end')

    print(old_password)
    print(new_password)
    print(repeated_new_password)


# function to handle add new hospital
def government_handle_add_hospital():
    # messagebox.showinfo('Info', 'Submitted succesffuly')

    hos_username1 = hos_username.get()
    hos_password1 = hos_password.get()
    hos_name1 = hos_name.get()
    hos_address1 = hos_address.get()
    hos_city1 = hos_city.get()
    hos_state1 = hos_state.get()
    hos_patient_count1 = hos_patient_count.get()
    hos_patient_cap1 = hos_patient_cap.get()
    hos_admited_count1 = hos_admited_count.get()
    hos_ventilater1 = hos_ventilater.get()

    '''hos_username.delete(0, 'end')
    hos_password.delete(0, 'end')
    hos_name.delete(0, 'end')
    hos_address.delete(0, 'end')
    hos_city.delete(0, 'end')
    hos_state.delete(0, 'end')
    hos_patient_count.delete(0, 'end')
    hos_patient_cap.delete(0, 'end')
    hos_admited_count.delete(0, 'end')
    hos_ventilater.delete(0, 'end')'''

    # all are working but values problem
    # start firstly
    # all are working but values problem
    # start firstly
    if hos_username.get() == "" or hos_password.get() == "" or hos_name.get() == "" or hos_address.get() == "" or hos_city.get() == "" or hos_state.get() == "" or hos_patient_count.get() == "" or hos_patient_cap.get() == "" or hos_admited_count.get() == "" or hos_ventilater.get() == "":
        messagebox.showerror("Error", "All fields are required")
        hos_username.delete(0, 'end')
        hos_password.delete(0, 'end')
        hos_name.delete(0, 'end')
        hos_address.delete(0, 'end')
        hos_city.delete(0, 'end')
        hos_state.delete(0, 'end')
        hos_patient_count.delete(0, 'end')
        hos_patient_cap.delete(0, 'end')
        hos_admited_count.delete(0, 'end')
        hos_ventilater.delete(0, 'end')
    else:

        try:
            query = "insert into hospitals(hospital_id, hospital_name, patient_capacity, total_patient_admitted_count, " \
                    "total_ventilators, address, city, state,state_id, password) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            print("query is ok")
            data = (hos_username1, hos_name1, hos_patient_cap1, hos_admited_count1, hos_ventilater1, hos_address1,
                    hos_city1, hos_state1, Government.government_details['state_id'], hos_password1)
            print("data is ok")
            cursor.execute(query, data)
            cnx.commit()
            messagebox.showinfo("information", "Record inserted successfully......")
            hos_username.delete(0, 'end')
            hos_password.delete(0, 'end')
            hos_name.delete(0, 'end')
            hos_address.delete(0, 'end')
            hos_city.delete(0, 'end')
            hos_state.delete(0, 'end')
            hos_patient_count.delete(0, 'end')
            hos_patient_cap.delete(0, 'end')
            hos_admited_count.delete(0, 'end')
            hos_ventilater.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", "Exception has been occur while Inserting")
            hos_username.delete(0, 'end')
            hos_password.delete(0, 'end')
            hos_name.delete(0, 'end')
            hos_address.delete(0, 'end')
            hos_city.delete(0, 'end')
            hos_state.delete(0, 'end')
            hos_patient_count.delete(0, 'end')
            hos_patient_cap.delete(0, 'end')
            hos_admited_count.delete(0, 'end')
            hos_ventilater.delete(0, 'end')
            print(e)

    print(hos_username1)
    print(hos_password1)
    print(hos_name1)
    print(hos_address1)
    print(hos_city1)
    print(hos_state1)
    print(hos_patient_count1)
    print(hos_patient_cap1)
    print(hos_admited_count1)
    print(hos_ventilater1)


# function to handle add new government
def government_handle_add_government():
    # messagebox.showinfo('Info', 'Submitted succesffuly')

    username = gov_username.get()
    gov_password = password.get()
    gov_name = government_name.get()
    state = government_state.get()

    if gov_username.get() == "" or password.get() == "" or government_name.get() == "" or government_state.get() == "":
        messagebox.showerror("Error", "All fields are required")

        gov_username.delete(0, 'end')
        password.delete(0, 'end')
        government_name.delete(0, 'end')
        government_state.delete(0, 'end')


    else:
        print("user name")
        print(username)
        print(Government.government_details['state_id'])
        try:
            if username == Government.government_details['state_id']:

                messagebox.showerror("Error", "Username Already Exist..")
                gov_username.delete(0, 'end')
                password.delete(0, 'end')
                government_name.delete(0, 'end')
                government_state.delete(0, 'end')
            else:
                query = "insert into government values(%s,%s,%s,%s);"
                print("query is ok")
                data = (username, gov_password, state, gov_name)
                cursor.execute(query, data)
                cnx.commit()
                messagebox.showinfo("information", "Record inserted successfully......")
                gov_username.delete(0, 'end')
                password.delete(0, 'end')
                government_name.delete(0, 'end')
                government_state.delete(0, 'end')

            #    messagebox.showerror("Error","Username Already Exist..")
            #   gov_username.delete(0, 'end')
            #  password.delete(0, 'end')
            # government_name.delete(0, 'end')
            # government_state.delete(0, 'end')

        except Exception as e:
            print(e)

            gov_username.delete(0, 'end')
            password.delete(0, 'end')
            government_name.delete(0, 'end')
            government_state.delete(0, 'end')
            messagebox.showerror("Error", "Exception has been occur...")
        print(username)
        print(gov_password)
        print(gov_name)
        print(state)


# function to search data by city
def search_by_city():
    city_name = searchby_city.get()
    searchby_city.delete(0, 'end')
    print(city_name)


'''
Actual Frames
'''


# function to create government signin frame
def government_signin():
    global government_frame
    global government_username_entry
    global government_password_entry

    government_frame = Frame(root, width=800, height=600)
    government_frame.pack_propagate(0)

    display_header("Government", "Back", "#00A439", 221,
                   government_frame, main_options)

    # Hospitals signup frame
    government_signup_frame = Frame(
        government_frame, bg="#e0e0e0", width=450, height=400, pady=10)
    government_signup_frame.grid_propagate(0)

    government_username_label = Label(
        government_signup_frame, bg="#e0e0e0", text="State Id", font=("calibri", 14))
    government_username_entry = Entry(government_signup_frame, width=30, font=("calibri", 16), bd=1,
                                      relief="groove", highlightbackground="red", highlightcolor="red", bg="#ffffff")
    government_password_label = Label(
        government_signup_frame, bg="#e0e0e0", text="Password", font=("calibri", 14))
    government_password_entry = Entry(government_signup_frame, width=30, show='*', font=("calibri", 16), bd=1,
                                      highlightbackground="red", highlightcolor="red", bg="#f9f9f9", relief="groove")

    government_submit = Button(government_signup_frame, text="Submit", width=15, height=2,
                               command=handle_government_signin, bd=1)

    Label(government_signup_frame, text="Sign In", font=(
        "calibri", 18, "bold"), bg="#e0e0e0").pack(padx=10, pady=25)

    # Pack items
    government_username_label.pack(padx=10, pady=2)
    government_username_entry.pack(padx=30, pady=2)
    Label(government_signup_frame, bg="#e0e0e0").pack(padx=10, pady=6)
    government_password_label.pack(padx=10, pady=2)
    government_password_entry.pack(padx=30, pady=2)
    Label(government_signup_frame, bg="#e0e0e0").pack(padx=10, pady=6)
    government_submit.pack(padx=10, pady=2)
    Label(government_signup_frame, bg="#e0e0e0").pack(padx=10, pady=15)

    government_signup_frame.pack(pady=80)

    government_frame.pack()


# function to create government dashboard frame
def government_dashboard():
    global government_dashboard_frame
    global searchby_city

    print("\nGovernment: ", Government.government_details)
    print("\ngovernmentIsLogin: ", Government.isLogin)

    government_dashboard_frame = Frame(root, width=800, height=600)
    government_dashboard_frame.pack_propagate(0)

    header = Frame(government_dashboard_frame, bg="#0000ff", height=53)
    header.pack_propagate(0)

    header_contents = Frame(header, height=50, pady=10, bg="#e9e9e9")
    header_contents.pack_propagate(0)

    Button(header_contents, text="Logout", bd=0, bg="#EC0000", fg="#ffffff",
           width=10, height=3, font=("calibri", 12),
           command=handle_government_logout). \
        pack(side=LEFT, padx=20)

    Label(header_contents, text="Government Dashboard", font=("calibri", 16, "bold"), bg="#e9e9e9"). \
        pack(side=LEFT, padx=175)

    header_contents.pack(fill=X)

    header.pack(fill=X)

    dashboard_information_container = Frame(
        government_dashboard_frame, width=800, height=162, bg="#0000ff")
    dashboard_information_container.pack_propagate(0)

    dashboard_information_left_frame = Frame(dashboard_information_container, width=400, height=160,
                                             padx=20, pady=30)
    dashboard_information_left_frame.grid_propagate(0)

    government_name_label = Label(dashboard_information_left_frame, text="Government Name", width=15, anchor='w',
                                  font=("calibri", 14), pady=0)
    government_state_label = Label(dashboard_information_left_frame, text="State", width=15, anchor='w',
                                   font=("calibri", 14), pady=0)
    patient_count_label = Label(dashboard_information_left_frame, text="Patient Count", width=15, anchor='w',
                                font=("calibri", 14), pady=0)
    searchby_city_label = Label(dashboard_information_left_frame, text="Search By City", width=15, anchor='w',
                                font=("calibri", 14), pady=3)

    government_name = Label(dashboard_information_left_frame, text=": " + Government.government_details['name'],
                            font=("calibri", 14), anchor='w', width=26, pady=3)
    government_state = Label(dashboard_information_left_frame, text=": " + Government.government_details['state'],
                             font=("calibri", 14), anchor='w', width=26, pady=3)
    patient_count = Label(dashboard_information_left_frame,
                          text=": " + str(Government.government_details['patient_count']),
                          font=("calibri", 14), anchor='w', width=26, pady=3)
    searchby_city = Entry(dashboard_information_left_frame,
                          width=24, font=("calibri", 14), relief=SOLID, highlightbackground="red", highlightcolor="red")
    search_city = Button(dashboard_information_left_frame, text="Search", width=7, height=1, relief=SOLID,
                         highlightbackground="red", highlightcolor="red",
                         command=search_by_city, bd=1)

    government_name_label.grid(row=0, column=0)
    government_state_label.grid(row=1, column=0)
    patient_count_label.grid(row=2, column=0)
    # searchby_city_label.grid(row=3, column=0)

    government_name.grid(row=0, column=2)
    government_state.grid(row=1, column=2)
    patient_count.grid(row=2, column=2)
    # searchby_city.grid(row=3, column=2)
    # search_city.grid(row=3, column=3)

    dashboard_information_right_frame = Frame(dashboard_information_container, width=400, height=160,
                                              padx=20, pady=30)
    dashboard_information_right_frame.grid_propagate(0)

    hospital_patient_capacity_label = Label(dashboard_information_right_frame, text="Patient Capacity", width=19,
                                            font=("calibri", 14), anchor='w', pady=3)
    hospital_admitted_count_label = Label(dashboard_information_right_frame, text="Admitted Count", width=19,
                                          font=("calibri", 14), anchor='w', pady=3)
    hospital_ventilators_count_label = Label(dashboard_information_right_frame, text="Ventilators Count", width=19,
                                             font=("calibri", 14), anchor='w', pady=3)

    hospital_patient_capacity = Label(dashboard_information_right_frame,
                                      text=":  " +
                                           str(
                                               Government.government_details['patient_capacity']),
                                      font=("calibri", 14), anchor='w', width=15, pady=3)
    hospital_admitted_count = Label(dashboard_information_right_frame,
                                    text=":  " +
                                         str(
                                             Government.government_details['patient_admitted_count']),
                                    font=("calibri", 14), anchor='w', width=15, pady=3)
    hospital_ventilators_count = Label(dashboard_information_right_frame,
                                       text=":  " +
                                            str(
                                                Government.government_details['ventilators_count']),
                                       font=("calibri", 14), anchor='w', width=15, pady=3)

    hospital_patient_capacity_label.grid(row=1, column=0)
    hospital_admitted_count_label.grid(row=2, column=0)
    hospital_ventilators_count_label.grid(row=3, column=0)

    hospital_patient_capacity.grid(row=1, column=2)
    hospital_admitted_count.grid(row=2, column=2)
    hospital_ventilators_count.grid(row=3, column=2)

    dashboard_information_container.pack()

    dashboard_information_left_frame.pack(side=LEFT, padx=(0, 1), pady=(0, 1))
    dashboard_information_right_frame.pack(padx=(2, 0))

    # Control Panel
    Label(government_dashboard_frame, font=("calibri", 16, "bold"),
          text="Controls").pack(pady=(20, 10))

    # 3 options
    dashboard_options_container_1 = Frame(government_dashboard_frame)

    if Government.government_details['state_id'] == "admin":
        Button(dashboard_options_container_1, text="Add Government", width=18, height=3, bg="#008CE1", fg="#ffffff",
               bd=0,
               relief="groove", font=("calibri", 17, "bold"),
               command=lambda: show_and_destroy_frame(government_add_government, government_dashboard_frame)) \
            .pack(padx=10, pady=10, side=LEFT)
        Button(dashboard_options_container_1, text="Display Governments", width=18, height=3, bg="#008CE1",
               fg="#ffffff",
               bd=0,
               relief="groove", font=("calibri", 17, "bold"),
               command=lambda: show_and_destroy_frame(display_governments, government_dashboard_frame)) \
            .pack(padx=10, pady=10, side=LEFT)
    else:
        Button(dashboard_options_container_1, text="Add Hospital", width=18, height=3, bg="#008CE1", fg="#ffffff", bd=0,
               relief="groove", font=("calibri", 17, "bold"),
               command=lambda: show_and_destroy_frame(government_add_hospital, government_dashboard_frame)).pack(
            padx=10,
            pady=10,
            side=LEFT)
    Button(dashboard_options_container_1, text="Change Password", width=18, height=3, bg="#008CE1", fg="#ffffff", bd=0,
           relief="groove", font=("calibri", 17, "bold"),
           command=lambda: show_and_destroy_frame(government_change_password, government_dashboard_frame)).pack(padx=10,
                                                                                                                pady=10,
                                                                                                                side=LEFT)
    dashboard_options_container_1.pack()

    dashboard_options_container_2 = Frame(government_dashboard_frame)
    Button(dashboard_options_container_2, text="Display Patients", width=18, height=3, bg="#008CE1", fg="#ffffff", bd=0,
           relief="groove", font=("calibri", 17, "bold"),
           command=lambda: show_and_destroy_frame(display_patients, government_dashboard_frame)) \
        .pack(padx=10, pady=10, side=LEFT)
    Button(dashboard_options_container_2, text="Display Hospitals", width=18, height=3, bg="#008CE1", fg="#ffffff",
           bd=0,
           relief="groove", font=("calibri", 17, "bold"),
           command=lambda: show_and_destroy_frame(display_hospitals, government_dashboard_frame)) \
        .pack(padx=10, pady=10, side=LEFT)
    dashboard_options_container_2.pack()

    government_dashboard_frame.pack()


# function to create add new government frame
def government_add_government():
    global add_government_frame
    global government_name
    global government_state
    global password
    global gov_username

    add_government_frame = Frame(root, width=800, height=600)
    add_government_frame.pack_propagate(0)

    display_header("Add Government", "Back", "#00A439", 205,
                   add_government_frame, government_dashboard)

    dashboard_options_container_1 = Frame(
        add_government_frame, bg="#e0e0e0", width=800, height=500, pady=25)

    user_name_label = Label(dashboard_options_container_1, text="State ID ", width=15, bd=1,
                            bg="#e0e0e0", font=("calibri", 14), pady=10)
    government_name_label = Label(dashboard_options_container_1, text="Government Name ", width=15, bd=1,
                                  bg="#e0e0e0", font=("calibri", 14), pady=10)
    government_state_label = Label(dashboard_options_container_1, text="State Name ", width=15, bd=1,
                                   bg="#e0e0e0", font=("calibri", 14), pady=10)
    password_label = Label(dashboard_options_container_1, text="Password", width=15,
                           bg="#e0e0e0", font=("calibri", 14), pady=10)
    pass_label = Label(dashboard_options_container_1, text="", width=15,
                       bg="#e0e0e0", font=("calibri", 14), pady=10)

    gov_username = Entry(dashboard_options_container_1, width=30, font=(
        "calibri", 14), relief="groove", bd=1)
    government_name = Entry(dashboard_options_container_1, width=30, font=(
        "calibri", 14), relief="groove", bd=1)
    government_state = Entry(dashboard_options_container_1, width=30, font=(
        "calibri", 14), relief="groove", bd=1)
    password = Entry(dashboard_options_container_1, width=30, font=(
        "calibri", 14), relief="groove", show="*", bd=1)

    user_name_label.pack(padx=10)
    gov_username.pack(padx=30, pady=2)

    government_name_label.pack(padx=10, pady=2)
    government_name.pack(padx=30, pady=2)

    government_state_label.pack(padx=10, pady=2)
    government_state.pack(padx=30, pady=2)

    password_label.pack(padx=10, pady=2)
    password.pack(padx=30, pady=2)

    hospitals_submit = Button(dashboard_options_container_1, text="Submit", fg="#ffffff", bg="#017700", width=15,
                              height=2,
                              command=government_handle_add_government, bd=1)

    hospitals_submit.pack(pady=(15, 0))

    dashboard_options_container_1.pack(pady=50)

    add_government_frame.pack()


# function to create add new hospitals frame
def government_add_hospital():
    global add_hospital_frame
    global hos_username
    global hos_password
    global hos_name
    global hos_address
    global hos_city
    global hos_state
    global hos_patient_count
    global hos_patient_cap
    global hos_admited_count
    global hos_ventilater

    add_hospital_frame = Frame(root, width=800, height=600)
    add_hospital_frame.pack_propagate(0)

    display_header("Add Hospital", "Back", "#00A439", 205,
                   add_hospital_frame, government_dashboard)

    dashboard_information = Frame(
        add_hospital_frame, bg="#e0e0e0", width=700, height=400, pady=20, padx=30)

    hospital_username_label = Label(dashboard_information, text="UserName", width=20, anchor='w',
                                    font=("calibri", 14), pady=6, bg="#e0e0e0")
    hospital_password_label = Label(dashboard_information, text="Password", width=20, anchor='w',
                                    font=("calibri", 14), pady=6, bg="#e0e0e0")
    hospital_name_label = Label(dashboard_information, text="Name", width=20, anchor='w',
                                font=("calibri", 14), pady=6, bg="#e0e0e0")
    hospital_address_label = Label(dashboard_information, text="Address", width=20, anchor='w',
                                   font=("calibri", 14), pady=6, bg="#e0e0e0")
    hospital_city_label = Label(dashboard_information, text="City", width=20, anchor='w',
                                font=("calibri", 14), pady=6, bg="#e0e0e0")
    hospital_state_label = Label(dashboard_information, text="State", width=20, anchor='w',
                                 font=("calibri", 14), pady=6, bg="#e0e0e0")
    hospital_patient_label = Label(dashboard_information, text="Patient Count", width=20, anchor='w',
                                   font=("calibri", 14), pady=6, bg="#e0e0e0")
    hospital_patient_cap_label = Label(dashboard_information, text="Patient Capacity", width=20, anchor='w',
                                       font=("calibri", 14), pady=6, bg="#e0e0e0")
    hospital_admitted_label = Label(dashboard_information, text="Admitted Count", width=20, anchor='w',
                                    font=("calibri", 14), pady=6, bg="#e0e0e0")
    hospital_ventilater_label = Label(dashboard_information, text="Ventilator Count", width=20, anchor='w',
                                      font=("calibri", 14), pady=6, bg="#e0e0e0")

    hos_username = Entry(dashboard_information, width=40, font=(
        "calibri", 14), relief="groove", bd=1)
    hos_password = Entry(dashboard_information, width=40, font=(
        "calibri", 14), relief="groove", bd=1)
    hos_name = Entry(dashboard_information, width=40, font=(
        "calibri", 14), relief="groove", bd=1)
    hos_address = Entry(dashboard_information, width=40, font=(
        "calibri", 14), relief="groove", bd=1)
    hos_city = Entry(dashboard_information, width=40, font=(
        "calibri", 14), relief="groove", bd=1)
    hos_state = Entry(dashboard_information, width=40, font=(
        "calibri", 14), relief="groove", bd=1)
    hos_patient_count = Entry(dashboard_information, width=40, font=(
        "calibri", 14), relief="groove", bd=1)
    hos_patient_cap = Entry(dashboard_information, width=40, font=(
        "calibri", 14), relief="groove", bd=1)
    hos_admited_count = Entry(dashboard_information, width=40, font=(
        "calibri", 14), relief="groove", bd=1)
    hos_ventilater = Entry(dashboard_information, width=40, font=(
        "calibri", 14), relief="groove", bd=1)

    hospital_username_label.grid(row=2, column=0)
    hospital_password_label.grid(row=4, column=0)
    hospital_name_label.grid(row=6, column=0)
    hospital_address_label.grid(row=8, column=0)
    hospital_city_label.grid(row=10, column=0)
    hospital_state_label.grid(row=12, column=0)
    hospital_patient_label.grid(row=14, column=0)
    hospital_patient_cap_label.grid(row=16, column=0)
    hospital_admitted_label.grid(row=18, column=0)
    hospital_ventilater_label.grid(row=20, column=0)

    hos_username.grid(row=2, column=1)
    hos_password.grid(row=4, column=1)
    hos_name.grid(row=6, column=1)
    hos_address.grid(row=8, column=1)
    hos_city.grid(row=10, column=1)
    hos_state.grid(row=12, column=1)
    hos_patient_count.grid(row=14, column=1)
    hos_patient_cap.grid(row=16, column=1)
    hos_admited_count.grid(row=18, column=1)
    hos_ventilater.grid(row=20, column=1)

    hospitals_submit = Button(dashboard_information, text="Submit", height=2, bd=0, bg="#017700", fg="#ffffff",
                              width=15,
                              command=government_handle_add_hospital, )

    hospitals_submit.grid(row=22, column=1, pady=(10, 0), padx=(0, 180))
    dashboard_information.pack(pady=40)

    add_hospital_frame.pack()


# function to create change government password frame
def government_change_password():
    global change_password_frame
    global change_password_old_password_entry1
    global change_password_new_password_entry1
    global change_password_repeated_new_password_entry1

    change_password_frame = Frame(root, width=800, height=600)
    change_password_frame.pack_propagate(0)

    display_header("Change Password", "Back", "#00A439", 200,
                   change_password_frame, government_dashboard)

    # Government change password frame
    government_change_password_container = Frame(
        change_password_frame, bg="#e0e0e0", width=450, height=400, pady=10)
    government_change_password_container.grid_propagate(0)

    change_password_old_password_label = Label(government_change_password_container, bg="#e0e0e0", text="Old Password",
                                               font=("calibri", 14))
    change_password_old_password_entry1 = Entry(government_change_password_container, width=30, font=("calibri", 16),
                                                bd=1, bg="#ffffff", relief="groove", show='*')

    change_password_new_password_label = Label(government_change_password_container, bg="#e0e0e0", text="New Password",
                                               font=("calibri", 14))
    change_password_new_password_entry1 = Entry(government_change_password_container, width=30, show='*',
                                                font=("calibri", 16), bd=1, bg="#f9f9f9", relief="groove")

    change_password_repeated_new_password_label = Label(government_change_password_container, bg="#e0e0e0",
                                                        text="Repeat New Password", font=("calibri", 14))
    change_password_repeated_new_password_entry1 = Entry(government_change_password_container, width=30, show='*',
                                                         font=("calibri", 16), bd=1, bg="#f9f9f9", relief="groove")

    password_update_button = Button(government_change_password_container, text="Update", width=15, height=2,
                                    command=government_handle_change_password, bd=1)

    # Pack items
    change_password_old_password_label.pack(padx=10, pady=2)
    change_password_old_password_entry1.pack(padx=30, pady=2)

    Label(government_change_password_container,
          bg="#e0e0e0").pack(padx=10, pady=4)

    change_password_new_password_label.pack(padx=10, pady=2)
    change_password_new_password_entry1.pack(padx=30, pady=2)

    Label(government_change_password_container,
          bg="#e0e0e0").pack(padx=10, pady=4)

    change_password_repeated_new_password_label.pack(padx=10, pady=2)
    change_password_repeated_new_password_entry1.pack(padx=30, pady=2)

    Label(government_change_password_container,
          bg="#e0e0e0").pack(padx=10, pady=5)

    password_update_button.pack(padx=10, pady=2)

    Label(government_change_password_container,
          bg="#e0e0e0").pack(padx=10, pady=15)

    government_change_password_container.pack(pady=80)

    change_password_frame.pack()


'''
-------------------------------------------------------------------------------------------------------
                                        HOSPITAL SECTION
-------------------------------------------------------------------------------------------------------
'''

'''
handle_frame_operations
'''


# function to handle hospital signin
def handle_hospital_signin():
    username = hospitals_username_entry.get()
    password = hospitals_password_entry.get()

    print(username)
    print(password)
    # hospital authentication
    if hospitals_username_entry.get() == "" or hospitals_password_entry.get() == "":
        messagebox.showerror("Error", "Both fields are required")
        hospitals_username_entry.delete(0, 'end')
        hospitals_password_entry.delete(0, 'end')
    else:
        try:
            query = "select * from hospitals where hospital_id = %s and password = %s ;"
            data = (username, password)
            print(username)
            cursor.execute(query, data)
            row = cursor.fetchone()
            print(row)
            if row == None:
                messagebox.showerror("Error", "Invalid Username or Password")
                hospitals_username_entry.delete(0, 'end')
                hospitals_password_entry.delete(0, 'end')
            else:
                data_set = row

                messagebox.showinfo("Information", "Welcome to Hospital  dashboard")
                hospitals_username_entry.delete(0, 'end')
                hospitals_password_entry.delete(0, 'end')
                print(row)

                print("Authorized..!")

                query = "select count(*) from patient where hospital_id = \"" + data_set[0] + "\";"
                cursor.execute(query)
                total_row_count = cursor.fetchall()[0]

                Hospital.set_hospital_details(data_set[0], data_set[1], data_set[2], total_row_count[0], data_set[3],
                                              data_set[4], data_set[5], data_set[6], data_set[7], data_set[8],
                                              data_set[9])
                Hospital.isLogin = True

                # show_and_hide_frame(government_dashboard_frame, government_frame)
                show_and_destroy_frame(hospital_dashboard, hospitals_frame)

        except mysql.connector.Error as err:
            print("Exception: ", err)
        except ValueError:
            print("Please enter input correctly..!")
        except KeyboardInterrupt:
            print("Please do not try to interrupt execution of program..!")
        except EOFError:
            print("Please enter input..!")
        except Exception as exc:
            print("Unexpected Exception: ", exc)


# function to handle hospital logout
def handle_hospital_logout():
    Hospital.set_hospital_details("", "", 0, 0, 0, 0, "", "", "", "", "")
    Hospital.isLogin = False
    show_and_destroy_frame(main_options, hospital_dashboard_frame)


# function to handle hospital update profile
def handle_update_profile():
    patient_capacity = update_profile_patient_capacity_entry.get()
    ventilators_count = update_profile_ventilators_count_entry.get()
    address = update_profile_address_entry.get()

    if update_profile_patient_capacity_entry.get() == "" or update_profile_ventilators_count_entry.get() == "" or update_profile_address_entry.get() == "":
        messagebox.showerror("Error", "Fields are Empty")
        update_profile_patient_capacity_entry.delete(0, 'end')
        update_profile_ventilators_count_entry.delete(0, 'end')
        update_profile_address_entry.delete(0, 'end')
    else:
        try:
            data = (patient_capacity, ventilators_count, address, Hospital.hospital_details['id'])
            query = "update hospitals set patient_capacity= %s,total_ventilators=%s,address=%s where hospital_id=%s ;"
            cursor.execute(query, data)
            cnx.commit()
            row = cursor.fetchone()
            print(row)
            Hospital.set_hospital_update_details(patient_capacity, ventilators_count, address)
            messagebox.showinfo("Information", "Profile Updated")
            update_profile_patient_capacity_entry.delete(0, 'end')
            update_profile_ventilators_count_entry.delete(0, 'end')
            update_profile_address_entry.delete(0, 'end')
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Error has been occur")
            update_profile_patient_capacity_entry.delete(0, 'end')
            update_profile_ventilators_count_entry.delete(0, 'end')
            update_profile_address_entry.delete(0, 'end')
    print(patient_capacity)
    print(ventilators_count)
    print(address)


# function to handle hospital add patient
def handle_add_patient():
    aadhar_no = hospital_add_patient_aadhar_no_entry.get()
    name = hospital_add_patient_name_entry.get()
    age = hospital_add_patient_age_entry.get()
    address = hospital_add_patient_address_entry.get()
    mobile_no = hospital_add_patient_mobile_no_entry.get()
    state = state_choice.get()
    city = city_choice.get()
    country = country_choice.get()

    # all are working but values problem
    if hospital_add_patient_aadhar_no_entry.get() == "" or hospital_add_patient_name_entry.get() == "" or hospital_add_patient_age_entry.get() == "" or hospital_add_patient_address_entry.get() == "" or hospital_add_patient_mobile_no_entry.get() == "" or state_choice.get() == "<--select-->" or state_choice.get() == "" or country_choice.get() == "<--select-->" or country_choice.get() == "" or city_choice.get() == "<--select-->" or city_choice.get() == "":
        messagebox.showerror("Error", "Fields are Empty")

        # hospital_add_patient_aadhar_no_entry.delete(0, 'end')
        # hospital_add_patient_name_entry.delete(0, 'end')
        # hospital_add_patient_age_entry.delete(0, 'end')
        # hospital_add_patient_address_entry.delete(0, 'end')
        # hospital_add_patient_mobile_no_entry.delete(0, 'end')
        # state_choice.set('<--select-->')
        # city_choice.set('<--select-->')
        # country_choice.set('<--select-->')
    else:

        try:

            query = "insert into patient_view (hospital_id,state_id,aadhar_no,full_name,age,address,mob_no,city,state,country) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            print("query is ok")
            data = (
                str(Hospital.hospital_details["id"]), str(Hospital.hospital_details["state_id"]), aadhar_no, name, age,
                address, mobile_no, state, city, country)
            cursor.execute(query, data)
            cnx.commit()
            messagebox.showinfo("information", "Record inserted successfully......")

            hospital_add_patient_aadhar_no_entry.delete(0, 'end')
            hospital_add_patient_name_entry.delete(0, 'end')
            hospital_add_patient_age_entry.delete(0, 'end')
            hospital_add_patient_address_entry.delete(0, 'end')
            hospital_add_patient_mobile_no_entry.delete(0, 'end')
            state_choice.set('<--select-->')
            city_choice.set('<--select-->')
            country_choice.set('<--select-->')
        except Exception as e:
            print("Exception has been occur while inserting", e)
            messagebox.showerror("Error", "Exception has been occur while inserting.." + str(e))
            hospital_add_patient_aadhar_no_entry.delete(0, 'end')
            hospital_add_patient_name_entry.delete(0, 'end')
            hospital_add_patient_age_entry.delete(0, 'end')
            hospital_add_patient_address_entry.delete(0, 'end')
            hospital_add_patient_mobile_no_entry.delete(0, 'end')
            state_choice.set('<--select-->')
            city_choice.set('<--select-->')
            country_choice.set('<--select-->')

    print(aadhar_no)
    print(name)
    print(age)
    print(address)
    print(mobile_no)
    print(state)
    print(city)
    print(country)


# function to handle hospital update patient
def handle_update_patient():
    aadhar_no = hospital_update_patient_aadhar_no_entry.get()
    covid_status = hospital_covid_status_choice.get()
    quarantine_type = hospital_quarantine_type_choice.get()
    positive_date = hospital_positive_date.get_date()
    negative_date = hospital_negative_date.get_date()
    admitted_date = hospital_admitted_date.get_date()
    discharge_date = hospital_discharge_date.get_date()
    dead_date = hospital_dead_date.get_date()

    if hospital_update_patient_aadhar_no_entry.get() == "":
        messagebox.showerror("Error", "Fields are Empty")
        hospital_update_patient_aadhar_no_entry.delete(0, 'end')
        hospital_covid_status_choice.set('<--select-->')
        hospital_quarantine_type_choice.set('<--select-->')
        hospital_positive_date.delete(0, 'end')
        hospital_negative_date.delete(0, 'end')
        hospital_admitted_date.delete(0, 'end')
        hospital_discharge_date.delete(0, 'end')
        hospital_dead_date.delete(0, 'end')
    else:

        try:
            fetch_old_record_query = "select * from patient where aadhar_no = " + str(aadhar_no) + ";"
            cursor.execute(fetch_old_record_query)
            old_record = cursor.fetchall()[0]

            if old_record[0] == Hospital.hospital_details['id']:
                if Hospital.isPositiveDateChanged:
                    print(positive_date)
                else:
                    positive_date = old_record[12]

                if Hospital.isNegativeDateChanged:
                    print(negative_date)
                else:
                    negative_date = old_record[16]

                if Hospital.isAdmittedDateChanged:
                    print(admitted_date)
                else:
                    admitted_date = old_record[15]

                if Hospital.isDischargeDateChanged:
                    print(discharge_date)
                else:
                    discharge_date = old_record[17]

                if Hospital.isDeadDateChanged:
                    print(dead_date)
                else:
                    dead_date = old_record[18]

                if quarantine_type == "<--select-->":
                    quarantine_type = old_record[13]

                if covid_status == "<--select-->":
                    covid_status = old_record[11]

                # messagebox.showinfo("information", "Need to update..!")
                query = "update patient set covid_status=%s, quarantine_type=%s ,positive_date=%s,negative_date=%s," \
                        "admitted_date=%s," \
                        "discharge_date=%s,dead_date=%s where aadhar_no=%s;"
                data = (
                    covid_status, quarantine_type, positive_date, negative_date, admitted_date, discharge_date,
                    dead_date,
                    aadhar_no)
                cursor.execute(query, data)
                cnx.commit()

                old_covid_status = old_record[11]
                old_quarantine_type = old_record[13]
                # old_admitted_status
                print("Old Covid Status: ", old_covid_status)
                print("Old Quarantine Type: ", old_quarantine_type)

                try:
                    # Covid Status (Positive and negative)
                    if old_covid_status is None and covid_status == "Positive":
                        update_query = "update hospitals set positive_count = positive_count + 1 where hospital_id=\"" + \
                                       Hospital.hospital_details['id'] + "\";"
                        cursor.execute(update_query)
                        cnx.commit()
                        print("Updated Patient Positive Count: ")
                    elif old_covid_status is None and covid_status == "Negative":
                        update_query = "update hospitals set negative_count = negative_count + 1 where hospital_id=\"" + \
                                       Hospital.hospital_details['id'] + "\";"
                        cursor.execute(update_query)
                        cnx.commit()
                        print("Updated Patient Negative Count: ")
                    elif old_covid_status == "Negative" and covid_status == "Positive":
                        update_query = "update hospitals set negative_count = negative_count - 1, " \
                                       "positive_count = positive_count + 1 where hospital_id=\"" + \
                                       Hospital.hospital_details['id'] + "\";"
                        cursor.execute(update_query)
                        cnx.commit()
                        print("Updated Patient Negative decreased and positive count increased: ")
                    elif old_covid_status == "Positive" and covid_status == "Negative":
                        update_query = "update hospitals set positive_count = positive_count - 1, " \
                                       "negative_count = negative_count + 1 where hospital_id=\"" + \
                                       Hospital.hospital_details['id'] + "\";"
                        cursor.execute(update_query)
                        cnx.commit()
                        print("Updated Patient Negative increased and positive count decreased: ")
                    else:
                        print("Covid Status Not Updated..!")

                    # Quarantine Type (Home and hospital)
                    if old_quarantine_type is None and quarantine_type == "Home Quarantine":
                        update_query = "update hospitals set home_quarantine_count = home_quarantine_count + 1 " \
                                       "where hospital_id=\"" + \
                                       Hospital.hospital_details['id'] + "\";"
                        cursor.execute(update_query)
                        cnx.commit()
                        print("Home Quarantine Increased")
                    elif old_quarantine_type is None and quarantine_type == "Hospital Quarantine":
                        update_query = "update hospitals set total_patient_admitted_count = " \
                                       "total_patient_admitted_count + 1 where hospital_id=\"" + \
                                       Hospital.hospital_details['id'] + "\";"
                        cursor.execute(update_query)
                        cnx.commit()
                        print("Hospital Quarantine Increased")
                    elif old_quarantine_type == "Hospital Quarantine" and quarantine_type == "Home Quarantine":
                        update_query = "update hospitals set total_patient_admitted_count = " \
                                       "total_patient_admitted_count - 1, " \
                                       "home_quarantine_count = home_quarantine_count + 1 where hospital_id=\"" + \
                                       Hospital.hospital_details['id'] + "\";"
                        cursor.execute(update_query)
                        cnx.commit()
                        print("Updated Hospital Quarantine decreased and Home Quarantine increased: ")
                    elif old_quarantine_type == "Home Quarantine" and quarantine_type == "Hospital Quarantine":
                        update_query = "update hospitals set home_quarantine_count = " \
                                       "home_quarantine_count - 1, " \
                                       "total_patient_admitted_count = " \
                                       "total_patient_admitted_count + 1 where hospital_id=\"" + \
                                       Hospital.hospital_details['id'] + "\";"
                        cursor.execute(update_query)
                        cnx.commit()
                        print("Updated Hospital Quarantine increased and Home Quarantine decreased: ")
                    else:
                        print("Quarantine Type not updated")

                    # Dead Count
                    if Hospital.isDeadDateChanged:
                        update_query = "update hospitals set dead_count = dead_count + 1 " \
                                       "where hospital_id=\"" + \
                                       Hospital.hospital_details['id'] + "\";"
                        cursor.execute(update_query)
                        cnx.commit()

                        if old_quarantine_type == "Home Quarantine":
                            update_query = "update hospitals set home_quarantine_count = home_quarantine_count - 1 " \
                                           "where hospital_id=\"" + \
                                           Hospital.hospital_details['id'] + "\";"
                            cursor.execute(update_query)
                            cnx.commit()
                            print("Home Quarantine Decreased")

                        if old_quarantine_type == "Hospital Quarantine":
                            update_query = "update hospitals set total_patient_admitted_count = " \
                                           "total_patient_admitted_count - 1 " \
                                           "where hospital_id=\"" + \
                                           Hospital.hospital_details['id'] + "\";"
                            cursor.execute(update_query)
                            cnx.commit()
                            print("Hospital Quarantine Decreased")

                        if old_covid_status == "Positive":
                            update_query = "update hospitals set positive_count = positive_count - 1 " \
                                           "where hospital_id=\"" + \
                                           Hospital.hospital_details['id'] + "\";"
                            cursor.execute(update_query)
                            cnx.commit()
                            print("Positive Count Decreased")

                        if old_covid_status == "Negative":
                            update_query = "update hospitals set negative_count = " \
                                           "negative_count - 1 " \
                                           "where hospital_id=\"" + \
                                           Hospital.hospital_details['id'] + "\";"
                            cursor.execute(update_query)
                            cnx.commit()
                            print("Negative Count Decreased")

                        print("Dead Count Increased updated")
                    else:
                        print("Dead Count not changed..!")
                except Exception as ee:
                    print(ee)

                messagebox.showinfo("information", "Record Updated successfully......")
            else:
                messagebox.showinfo("error", "Patient not present in your hospital..!")

            hospital_update_patient_aadhar_no_entry.delete(0, 'end')
            hospital_covid_status_choice.set('<--select-->')
            hospital_quarantine_type_choice.set('<--select-->')
            hospital_positive_date.delete(0, 'end')
            hospital_negative_date.delete(0, 'end')
            hospital_admitted_date.delete(0, 'end')
            hospital_discharge_date.delete(0, 'end')
            hospital_dead_date.delete(0, 'end')
            print(old_record)
        except Exception as e:
            print("Exception has been occur while inserting")
            hospital_update_patient_aadhar_no_entry.delete(0, 'end')
            hospital_covid_status_choice.set('<--select-->')
            hospital_quarantine_type_choice.set('<--select-->')
            hospital_positive_date.delete(0, 'end')
            hospital_negative_date.delete(0, 'end')
            hospital_admitted_date.delete(0, 'end')
            hospital_discharge_date.delete(0, 'end')
            hospital_dead_date.delete(0, 'end')

    print(aadhar_no)
    print(covid_status)
    print(quarantine_type)

    Hospital.isPositiveDateChanged = False
    Hospital.isNegativeDateChanged = False
    Hospital.isAdmittedDateChanged = False
    Hospital.isDischargeDateChanged = False
    Hospital.isDeadDateChanged = False


# function to handle hospital change password
def handle_hospital_change_password():
    old_password = change_password_old_password_entry.get()
    new_password = change_password_new_password_entry.get()
    repeated_new_password = change_password_repeated_new_password_entry.get()

    if change_password_old_password_entry.get() == "" or change_password_new_password_entry.get() == "" or change_password_repeated_new_password_entry.get() == "":
        messagebox.showerror("Error", "Fields are Empty")

        change_password_old_password_entry.delete(0, 'end')
        change_password_new_password_entry.delete(0, 'end')
        change_password_repeated_new_password_entry.delete(0, 'end')


    elif new_password != repeated_new_password:
        messagebox.showerror("Error", "you enter different passwords ")

        change_password_old_password_entry.delete(0, 'end')
        change_password_new_password_entry.delete(0, 'end')
        change_password_repeated_new_password_entry.delete(0, 'end')

    elif new_password == repeated_new_password:

        try:
            print("*******************")
            print(Hospital.hospital_details['password'])
            if old_password == (Hospital.hospital_details['password']):

                data = (new_password, Hospital.hospital_details['id'])
                query = "update hospitals set password= %s where hospital_id=%s;"
                cursor.execute(query, data)
                cnx.commit()

                Hospital.hospital_details['password'] = new_password

                row = cursor.fetchone()
                print(row)
                messagebox.showinfo("Information", "Password has been changed...")
                change_password_old_password_entry.delete(0, 'end')
                change_password_new_password_entry.delete(0, 'end')
                change_password_repeated_new_password_entry.delete(0, 'end')
            else:
                messagebox.showerror("Error", "old password is Invalid..")
                change_password_old_password_entry.delete(0, 'end')
                change_password_new_password_entry.delete(0, 'end')
                change_password_repeated_new_password_entry.delete(0, 'end')

        except Exception as e:

            print(e)
            messagebox.showerror("Error", "exception occur")
            change_password_old_password_entry.delete(0, 'end')
            change_password_new_password_entry.delete(0, 'end')
            change_password_repeated_new_password_entry.delete(0, 'end')

    #    change_password_old_password_entry.delete(0, 'end')
    #  change_password_new_password_entry.delete(0, 'end')
    #    change_password_repeated_new_password_entry.delete(0, 'end')

    print(old_password)
    print(new_password)
    print(repeated_new_password)


# function to handle hospital change cities
def hospital_set_cities(e):
    city_choice["values"] = CITIES[state_choice.get()]
    city_choice.current(0)
    city_choice.set('<--select-->')


'''
Actual Frames
'''


# function to create hospital signin frame
def hospital_signin():
    global hospitals_frame
    global hospitals_username_entry
    global hospitals_password_entry

    # Hospital Frame
    hospitals_frame = Frame(root, width=800, height=600)
    hospitals_frame.pack_propagate(0)

    display_header("Hospital", "Back", "#00A439", 231,
                   hospitals_frame, main_options)

    # Hospitals signup frame
    hospital_signup_frame = Frame(
        hospitals_frame, bg="#e0e0e0", width=450, height=400, pady=10)
    hospital_signup_frame.grid_propagate(0)

    hospitals_username_label = Label(
        hospital_signup_frame, bg="#e0e0e0", text="Username:", font=("calibri", 14))
    hospitals_username_entry = Entry(hospital_signup_frame, width=30, font=("calibri", 16), bd=1,
                                     bg="#ffffff", relief="groove")
    hospitals_password_label = Label(
        hospital_signup_frame, bg="#e0e0e0", text="Password:", font=("calibri", 14))
    hospitals_password_entry = Entry(hospital_signup_frame, width=30, show='*', font=("calibri", 16), bd=1,
                                     bg="#f9f9f9", relief="groove")

    hospitals_submit = Button(hospital_signup_frame, text="Submit", width=15, height=2,
                              command=handle_hospital_signin, bd=1)

    Label(hospital_signup_frame, text="Sign In", font=(
        "calibri", 18, "bold"), bg="#e0e0e0").pack(padx=10, pady=25)

    # Pack items
    hospitals_username_label.pack(padx=10, pady=2)
    hospitals_username_entry.pack(padx=30, pady=2)
    Label(hospital_signup_frame, bg="#e0e0e0").pack(padx=10, pady=6)
    hospitals_password_label.pack(padx=10, pady=2)
    hospitals_password_entry.pack(padx=30, pady=2)
    Label(hospital_signup_frame, bg="#e0e0e0").pack(padx=10, pady=6)
    hospitals_submit.pack(padx=10, pady=2)
    Label(hospital_signup_frame, bg="#e0e0e0").pack(padx=10, pady=15)

    hospital_signup_frame.pack(pady=80)

    hospitals_frame.pack()


# function to create hospital dashboard frame
def hospital_dashboard():
    global hospital_dashboard_frame

    # Dashboard header
    hospital_dashboard_frame = Frame(root, width=800, height=600)
    hospital_dashboard_frame.pack_propagate(0)

    print("\nHospital: ", Hospital.hospital_details)
    print("\nhospitalIsLogin: ", Hospital.isLogin)

    header = Frame(hospital_dashboard_frame, bg="#0000ff", height=53)
    header.pack_propagate(0)

    header_contents = Frame(header, height=50, pady=10, bg="#e9e9e9")
    header_contents.pack_propagate(0)

    Button(header_contents, text="Logout", bd=0, bg="#EC0000", fg="#ffffff",
           width=10, height=3, font=("calibri", 12),
           command=handle_hospital_logout). \
        pack(side=LEFT, padx=20)

    Label(header_contents, text="Hospital Dashboard", font=("calibri", 16, "bold"), bg="#e9e9e9"). \
        pack(side=LEFT, padx=195)

    header_contents.pack(fill=X)

    header.pack(fill=X)

    # Dashboard Information
    dashboard_information_container = Frame(
        hospital_dashboard_frame, width=800, height=162, bg="#0000ff")
    dashboard_information_container.pack_propagate(0)

    # Left Information Frame
    dashboard_information_left_frame = Frame(dashboard_information_container, width=400, height=160,
                                             padx=20, pady=12)
    dashboard_information_left_frame.grid_propagate(0)

    hospital_name_label = Label(dashboard_information_left_frame, text="  Name", width=9, anchor='w',
                                font=("calibri", 14), pady=3)
    hospital_address_label = Label(dashboard_information_left_frame, text="  Address", width=9, anchor='w',
                                   font=("calibri", 14), pady=3)
    hospital_city_label = Label(dashboard_information_left_frame, text="  City", width=9, anchor='w',
                                font=("calibri", 14), pady=3)
    hospital_state_label = Label(dashboard_information_left_frame, text="  State", width=9, anchor='w',
                                 font=("calibri", 14), pady=3)

    hospital_name = Label(dashboard_information_left_frame, text=":  " + Hospital.hospital_details['name'],
                          font=("calibri", 14), anchor='w', width=26, pady=3)
    hospital_address = Label(dashboard_information_left_frame, text=":  " + Hospital.hospital_details['address'],
                             font=("calibri", 14), anchor='w', width=26, pady=3)
    hospital_city = Label(dashboard_information_left_frame, text=":  " + Hospital.hospital_details['city'],
                          font=("calibri", 14), anchor='w', width=26, pady=3)
    hospital_state = Label(dashboard_information_left_frame, text=":  " + Hospital.hospital_details['state'],
                           font=("calibri", 14), anchor='w', width=26, pady=3)

    hospital_name_label.grid(row=0, column=0)
    hospital_address_label.grid(row=1, column=0)
    hospital_city_label.grid(row=2, column=0)
    hospital_state_label.grid(row=3, column=0)

    hospital_name.grid(row=0, column=2)
    hospital_address.grid(row=1, column=2)
    hospital_city.grid(row=2, column=2)
    hospital_state.grid(row=3, column=2)

    # Right Information Frame
    dashboard_information_right_frame = Frame(dashboard_information_container, width=400, height=160,
                                              padx=20, pady=12)
    dashboard_information_right_frame.grid_propagate(0)

    hospital_patient_count_label = Label(dashboard_information_right_frame, text="  Patient Count", width=19,
                                         font=("calibri", 14), anchor='w', pady=3)
    hospital_patient_capacity_label = Label(dashboard_information_right_frame, text="  Patient Capacity", width=19,
                                            font=("calibri", 14), anchor='w', pady=3)
    hospital_admitted_count_label = Label(dashboard_information_right_frame, text="  Admitted Count", width=19,
                                          font=("calibri", 14), anchor='w', pady=3)
    hospital_ventilators_count_label = Label(dashboard_information_right_frame, text="  Ventilators Count", width=19,
                                             font=("calibri", 14), anchor='w', pady=3)

    hospital_patient_count = Label(dashboard_information_right_frame,
                                   text=":  " +
                                        str(
                                            Hospital.hospital_details['patient_count']),
                                   font=("calibri", 14), anchor='w', width=15, pady=3)
    hospital_patient_capacity = Label(dashboard_information_right_frame,
                                      text=":  " +
                                           str(
                                               Hospital.hospital_details['patient_capacity']),
                                      font=("calibri", 14), anchor='w', width=15, pady=3)
    hospital_admitted_count = Label(dashboard_information_right_frame,
                                    text=":  " +
                                         str(
                                             Hospital.hospital_details['patient_admitted_count']),
                                    font=("calibri", 14), anchor='w', width=15, pady=3)
    hospital_ventilators_count = Label(dashboard_information_right_frame,
                                       text=":  " +
                                            str(
                                                Hospital.hospital_details['ventilators_count']),
                                       font=("calibri", 14), anchor='w', width=15, pady=3)

    hospital_patient_count_label.grid(row=0, column=0)
    hospital_patient_capacity_label.grid(row=1, column=0)
    hospital_admitted_count_label.grid(row=2, column=0)
    hospital_ventilators_count_label.grid(row=3, column=0)

    hospital_patient_count.grid(row=0, column=2)
    hospital_patient_capacity.grid(row=1, column=2)
    hospital_admitted_count.grid(row=2, column=2)
    hospital_ventilators_count.grid(row=3, column=2)

    dashboard_information_container.pack()

    dashboard_information_left_frame.pack(side=LEFT, padx=(0, 1), pady=(0, 1))
    dashboard_information_right_frame.pack(padx=(2, 0))

    # Control Panel
    Label(hospital_dashboard_frame, font=("calibri", 16, "bold"),
          text="Controls").pack(pady=(20, 10))

    # first 3 options
    dashboard_options_container_1 = Frame(hospital_dashboard_frame)
    Button(dashboard_options_container_1, text="Update Profile", width=18, height=3, bg="#008CE1", fg="#ffffff", bd=0,
           relief="groove", font=("calibri", 17, "bold"),
           command=lambda: show_and_destroy_frame(hospital_update_profile, hospital_dashboard_frame)) \
        .pack(padx=10, pady=10, side=LEFT)
    Button(dashboard_options_container_1, text="Add Patient", width=18, height=3, bg="#008CE1", fg="#ffffff", bd=0,
           relief="groove", font=("calibri", 17, "bold"),
           command=lambda: show_and_destroy_frame(hospital_add_patient, hospital_dashboard_frame)).pack(padx=10,
                                                                                                        pady=10,
                                                                                                        side=LEFT)
    Button(dashboard_options_container_1, text="Update Patient", width=18, height=3, bg="#008CE1", fg="#ffffff", bd=0,
           relief="groove", font=("calibri", 17, "bold"),
           command=lambda: show_and_destroy_frame(hospital_update_patient, hospital_dashboard_frame)).pack(padx=10,
                                                                                                           pady=10,
                                                                                                           side=LEFT)

    # another 3 options
    dashboard_options_container_2 = Frame(hospital_dashboard_frame)
    Button(dashboard_options_container_2, text="Display Patients", width=18, height=3, bg="#008CE1", fg="#ffffff", bd=0,
           relief="groove", font=("calibri", 17, "bold"),
           command=lambda: show_and_destroy_frame(display_patients, hospital_dashboard_frame)) \
        .pack(padx=10, pady=10, side=LEFT)
    # Button(dashboard_options_container_2, text="Statistics", width=18, height=3, bg="#008CE1", fg="#ffffff", bd=0,
    #        relief="groove", font=("calibri", 17, "bold"),
    #        command=lambda: show_and_destroy_frame(statistics, hospital_dashboard_frame)) \
    #     .pack(padx=10, pady=10, side=LEFT)
    Button(dashboard_options_container_2, text="Change Password", width=18, height=3, bg="#008CE1", fg="#ffffff", bd=0,
           relief="groove", font=("calibri", 17, "bold"),
           command=lambda: show_and_destroy_frame(hospital_change_password, hospital_dashboard_frame)) \
        .pack(padx=10, pady=10, side=LEFT)

    dashboard_options_container_1.pack()
    dashboard_options_container_2.pack()

    hospital_dashboard_frame.pack()


# function to create hospital update profile frame
def hospital_update_profile():
    global hospital_update_profile_frame
    global update_profile_patient_capacity_entry
    global update_profile_ventilators_count_entry
    global update_profile_address_entry

    hospital_update_profile_frame = Frame(root, width=800, height=600)
    hospital_update_profile_frame.pack_propagate(0)

    display_header("Update Profile", "Back", "#00A439", 215,
                   hospital_update_profile_frame, hospital_dashboard)

    # Hospitals change password frame
    hospital_update_profile_container = Frame(
        hospital_update_profile_frame, bg="#e0e0e0", width=450, height=400, pady=10)
    hospital_update_profile_container.grid_propagate(0)
    update_profile_patient_capacity_label = Label(hospital_update_profile_container, bg="#e0e0e0",
                                                  text="Patient Capacity", font=("calibri", 14))

    update_profile_patient_capacity_entry = Entry(hospital_update_profile_container, width=30, font=("calibri", 16),
                                                  bd=1, bg="#ffffff", relief="groove")

    update_profile_ventilators_count_label = Label(hospital_update_profile_container, bg="#e0e0e0",
                                                   text="Ventilators Count", font=("calibri", 14))
    update_profile_ventilators_count_entry = Entry(hospital_update_profile_container, width=30,
                                                   font=("calibri", 16), bd=1, bg="#f9f9f9", relief="groove")

    update_profile_address_label = Label(hospital_update_profile_container, bg="#e0e0e0",
                                         text="Address", font=("calibri", 14))
    update_profile_address_entry = Entry(hospital_update_profile_container, width=30,
                                         font=("Calibri", 16), bd=1, bg="#f9f9f9", relief="groove")

    password_update_button = Button(hospital_update_profile_container, text="Update", width=15, height=2,
                                    command=handle_update_profile, bd=1)

    # Pack items
    update_profile_patient_capacity_label.pack(padx=10, pady=2)
    update_profile_patient_capacity_entry.pack(padx=30, pady=2)

    Label(hospital_update_profile_container,
          bg="#e0e0e0").pack(padx=10, pady=4)

    update_profile_ventilators_count_label.pack(padx=10, pady=2)
    update_profile_ventilators_count_entry.pack(padx=30, pady=2)

    Label(hospital_update_profile_container,
          bg="#e0e0e0").pack(padx=10, pady=4)

    update_profile_address_label.pack(padx=10, pady=2)
    update_profile_address_entry.pack(padx=30, pady=2)

    Label(hospital_update_profile_container,
          bg="#e0e0e0").pack(padx=10, pady=5)

    password_update_button.pack(padx=10, pady=2)

    Label(hospital_update_profile_container,
          bg="#e0e0e0").pack(padx=10, pady=15)

    hospital_update_profile_container.pack(pady=80)

    hospital_update_profile_frame.pack()


# function to create hospital add patient frame
def hospital_add_patient():
    global hospital_add_patient_frame
    global hospital_add_patient_aadhar_no_entry
    global hospital_add_patient_name_entry
    global hospital_add_patient_age_entry
    global hospital_add_patient_address_entry
    global hospital_add_patient_mobile_no_entry
    global state_choice
    global city_choice
    global country_choice

    hospital_add_patient_frame = Frame(root, width=800, height=600)
    hospital_add_patient_frame.pack_propagate(0)

    display_header("Add Patient", "Back", "#00A439", 225,
                   hospital_add_patient_frame, hospital_dashboard)

    hospital_add_patient_form_container = Frame(
        hospital_add_patient_frame, width=800, height=355, bg="#d3d3d3")
    hospital_add_patient_form_container.pack_propagate(0)

    # -------------
    #   Left Side
    # -------------
    hospital_add_patient_left_frame = Frame(
        hospital_add_patient_form_container, width=400, pady=22)

    # Aadhar No
    hospital_add_patient_aadhar_no_label = Label(hospital_add_patient_left_frame,
                                                 text="Aadhar No", font=("calibri", 14))

    hospital_add_patient_aadhar_no_entry = Entry(hospital_add_patient_left_frame, width=30, font=("calibri", 16),
                                                 bd=1, bg="#ffffff", relief="groove")

    # Name
    hospital_add_patient_name_label = Label(hospital_add_patient_left_frame,
                                            text="Full Name", font=("calibri", 14))
    hospital_add_patient_name_entry = Entry(hospital_add_patient_left_frame, width=30,
                                            font=("calibri", 16), bd=1, bg="#f9f9f9", relief="groove")

    # Age
    hospital_add_patient_age_label = Label(hospital_add_patient_left_frame,
                                           text="Age", font=("calibri", 14))
    hospital_add_patient_age_entry = Entry(hospital_add_patient_left_frame, width=30,
                                           font=("Calibri", 16), bd=1, bg="#f9f9f9", relief="groove")

    # Address
    hospital_add_patient_address_label = Label(hospital_add_patient_left_frame,
                                               text="Address", font=("calibri", 14))
    hospital_add_patient_address_entry = Entry(hospital_add_patient_left_frame, width=30,
                                               font=("Calibri", 16), bd=1, bg="#f9f9f9", relief="groove")

    # Pack Items
    hospital_add_patient_aadhar_no_label.pack(padx=10, pady=2)
    hospital_add_patient_aadhar_no_entry.pack(padx=32, pady=(2, 11))

    hospital_add_patient_name_label.pack(padx=10, pady=2)
    hospital_add_patient_name_entry.pack(padx=32, pady=(2, 11))

    hospital_add_patient_age_label.pack(padx=10, pady=2)
    hospital_add_patient_age_entry.pack(padx=32, pady=(2, 11))

    hospital_add_patient_address_label.pack(padx=10, pady=2)
    hospital_add_patient_address_entry.pack(padx=32, pady=(2, 12))

    # -------------
    #   Right Side
    # -------------

    hospital_add_patient_right_frame = Frame(
        hospital_add_patient_form_container, width=400, pady=24)

    # Address
    hospital_add_patient_mobile_no_label = Label(hospital_add_patient_right_frame,
                                                 text="Mobile No", font=("calibri", 14))
    hospital_add_patient_mobile_no_entry = Entry(hospital_add_patient_right_frame, width=30,
                                                 font=("Calibri", 16), bd=1, bg="#f9f9f9", relief="groove")

    # State
    hospital_add_patient_state_label = Label(hospital_add_patient_right_frame,
                                             text="State", font=("calibri", 14))
    state_choice = ttk.Combobox(hospital_add_patient_right_frame, values=STATES, state="readonly", width=31,
                                font=("calibri", 14))
    state_choice.bind("<<ComboboxSelected>>", hospital_set_cities)
    state_choice.set("<--select-->")

    # City
    hospital_add_patient_city_label = Label(hospital_add_patient_right_frame,
                                            text="City", font=("calibri", 14))
    city_choice = ttk.Combobox(hospital_add_patient_right_frame, values=[], state="readonly", width=31,
                               font=("calibri", 14))
    city_choice.set("<--select-->")

    # Country
    hospital_add_patient_country_label = Label(hospital_add_patient_right_frame,
                                               text="Country", font=("calibri", 14))
    country_choice = ttk.Combobox(hospital_add_patient_right_frame, values=COUNTRIES, state="readonly", width=31,
                                  font=("calibri", 14))
    country_choice.set("<--select-->")

    # Pack Items
    hospital_add_patient_mobile_no_label.pack(padx=10, pady=2)
    hospital_add_patient_mobile_no_entry.pack(padx=32, pady=(2, 11))

    hospital_add_patient_state_label.pack(padx=10, pady=2)
    state_choice.pack(padx=32, pady=(2, 11))

    hospital_add_patient_city_label.pack(padx=10, pady=2)
    city_choice.pack(padx=32, pady=(2, 11))

    hospital_add_patient_country_label.pack(padx=10, pady=2)
    country_choice.pack(padx=32, pady=(2, 11))

    # Frame Pack
    hospital_add_patient_left_frame.pack(side=LEFT, padx=(0, 0), pady=(0, 0))
    hospital_add_patient_right_frame.pack(side=RIGHT, padx=(0, 0))
    hospital_add_patient_form_container.pack(pady=(60, 0))

    # Add Button
    Button(hospital_add_patient_frame, text="Add", width=15, height=1, bd=0, bg="#017700", fg="#ffffff",
           command=handle_add_patient,
           font=("calibri", 14, "bold")).pack(pady=(44, 0))

    hospital_add_patient_frame.pack()


# function to create hospital update patient frame
def hospital_update_patient():
    global hospital_update_patient_frame
    global hospital_update_patient_aadhar_no_entry
    global hospital_covid_status_choice
    global hospital_quarantine_type_choice
    global hospital_positive_date
    global hospital_negative_date
    global hospital_admitted_date
    global hospital_discharge_date
    global hospital_dead_date

    hospital_update_patient_frame = Frame(root, width=800, height=600)
    hospital_update_patient_frame.pack_propagate(0)

    display_header("Update Patient", "Back", "#00A439", 205,
                   hospital_update_patient_frame, hospital_dashboard)

    hospital_update_patient_form_container = Frame(
        hospital_update_patient_frame, width=800, height=355, bg="#d3d3d3")
    hospital_update_patient_form_container.pack_propagate(0)

    # -------------
    #   Left Side
    # -------------
    hospital_update_patient_left_frame = Frame(
        hospital_update_patient_form_container, width=400, pady=24)

    # Aadhar No
    hospital_update_patient_aadhar_no_label = Label(hospital_update_patient_left_frame,
                                                    text="Aadhar No", font=("calibri", 14))

    hospital_update_patient_aadhar_no_entry = Entry(hospital_update_patient_left_frame, width=30, font=("calibri", 16),
                                                    bd=1, bg="#ffffff", relief="groove")

    # Covid Status
    hospital_update_patient_covid_status_label = Label(hospital_update_patient_left_frame,
                                                       text="Covid Status", font=("calibri", 14))

    hospital_covid_status_choice = ttk.Combobox(hospital_update_patient_left_frame, values=["Positive", "Negative"],
                                                state="readonly",
                                                width=31,
                                                font=("calibri", 14))
    hospital_covid_status_choice.set("<--select-->")

    # Quarantine Type
    hospital_update_patient_quarantine_type_label = Label(hospital_update_patient_left_frame,
                                                          text="Quarantine Type", font=("calibri", 14))
    hospital_quarantine_type_choice = ttk.Combobox(hospital_update_patient_left_frame,
                                                   values=[
                                                       "Home Quarantine", "Hospital Quarantine"],
                                                   state="readonly",
                                                   width=31,
                                                   font=("calibri", 14))
    hospital_quarantine_type_choice.set("<--select-->")

    # Positive Date
    hospital_update_positive_date_label = Label(hospital_update_patient_left_frame,
                                                text="Positive Date", font=("calibri", 14))
    hospital_positive_date = DateEntry(hospital_update_patient_left_frame, selectmode='day',
                                       width=31, date_pattern='dd/mm/yyyy',
                                       font=("calibri", 14)
                                       )

    # Pack Items
    hospital_update_patient_aadhar_no_label.pack(padx=10, pady=2)
    hospital_update_patient_aadhar_no_entry.pack(padx=33, pady=(2, 11))

    hospital_update_patient_covid_status_label.pack(padx=10, pady=2)
    hospital_covid_status_choice.pack(padx=33, pady=(2, 11))

    hospital_update_patient_quarantine_type_label.pack(padx=10, pady=2)
    hospital_quarantine_type_choice.pack(padx=33, pady=(2, 11))

    hospital_update_positive_date_label.pack(padx=10, pady=2)
    hospital_positive_date.pack(padx=33, pady=(2, 12))

    # -------------
    #   Right Side
    # -------------
    hospital_update_patient_right_frame = Frame(
        hospital_update_patient_form_container, width=400, pady=25)

    # Negative Date
    hospital_update_positive_date_label = Label(hospital_update_patient_right_frame,
                                                text="Negative Date", font=("calibri", 14))
    hospital_negative_date = DateEntry(hospital_update_patient_right_frame, selectmode='day',
                                       width=31, date_pattern='dd/mm/yyyy',
                                       font=("calibri", 14)
                                       )
    # Admitted date
    hospital_update_admitted_date_label = Label(hospital_update_patient_right_frame,
                                                text="Admitted Date", font=("calibri", 14))
    hospital_admitted_date = DateEntry(hospital_update_patient_right_frame, selectmode='day',
                                       width=31, date_pattern='dd/mm/yyyy',
                                       font=("calibri", 14)
                                       )

    # Discharge Date
    hospital_update_discharge_date_label = Label(hospital_update_patient_right_frame,
                                                 text="Discharge Date", font=("calibri", 14))
    hospital_discharge_date = DateEntry(hospital_update_patient_right_frame, selectmode='day',
                                        width=31, date_pattern='dd/mm/yyyy',
                                        font=("calibri", 14)
                                        )

    # Dead Date
    hospital_update_dead_date_label = Label(hospital_update_patient_right_frame,
                                            text="Dead Date", font=("calibri", 14))
    hospital_dead_date = DateEntry(hospital_update_patient_right_frame, selectmode='day',
                                   width=31, date_pattern='dd/mm/yyyy',
                                   font=("calibri", 14)
                                   )

    # update dates
    hospital_positive_date.delete(0, 'end')
    hospital_negative_date.delete(0, 'end')
    hospital_admitted_date.delete(0, 'end')
    hospital_discharge_date.delete(0, 'end')
    hospital_dead_date.delete(0, 'end')

    hospital_positive_date.bind(
        "<<DateEntrySelected>>", Hospital.positive_date_changed)
    hospital_negative_date.bind(
        "<<DateEntrySelected>>", Hospital.negative_date_changed)
    hospital_admitted_date.bind(
        "<<DateEntrySelected>>", Hospital.admitted_date_changed)
    hospital_discharge_date.bind(
        "<<DateEntrySelected>>", Hospital.discharge_date_changed)
    hospital_dead_date.bind("<<DateEntrySelected>>",
                            Hospital.dead_date_changed)

    # Pack Items
    hospital_update_positive_date_label.pack(padx=10, pady=2)
    hospital_negative_date.pack(padx=32, pady=(2, 11))

    hospital_update_admitted_date_label.pack(padx=10, pady=2)
    hospital_admitted_date.pack(padx=32, pady=(2, 11))

    hospital_update_discharge_date_label.pack(padx=10, pady=2)
    hospital_discharge_date.pack(padx=32, pady=(2, 11))

    hospital_update_dead_date_label.pack(padx=10, pady=2)
    hospital_dead_date.pack(padx=32, pady=(2, 11))

    # Frame Pack
    hospital_update_patient_left_frame.pack(
        side=LEFT, padx=(0, 0), pady=(0, 0))
    hospital_update_patient_right_frame.pack(side=RIGHT, padx=(0, 0))
    hospital_update_patient_form_container.pack(pady=(60, 0))

    # Add Button
    Button(hospital_update_patient_frame, text="Update", width=15, height=1, bd=0, bg="#017700", fg="#ffffff",
           command=handle_update_patient,
           font=("calibri", 14, "bold")).pack(pady=(44, 0))

    hospital_update_patient_frame.pack()


# function to create hospital change password frame
def hospital_change_password():
    global hospital_change_password_frame
    global change_password_old_password_entry
    global change_password_new_password_entry
    global change_password_repeated_new_password_entry

    hospital_change_password_frame = Frame(root, width=800, height=600)
    hospital_change_password_frame.pack_propagate(0)

    display_header("Change Password", "Back", "#00A439", 200,
                   hospital_change_password_frame, hospital_dashboard)

    # Hospitals change password frame
    hospital_change_password_container = Frame(hospital_change_password_frame, bg="#e0e0e0", width=450, height=400,
                                               pady=10)
    hospital_change_password_container.grid_propagate(0)

    change_password_old_password_label = Label(hospital_change_password_container, bg="#e0e0e0", text="Old Password",
                                               font=("calibri", 14))
    change_password_old_password_entry = Entry(hospital_change_password_container, width=30, font=("calibri", 16),
                                               bd=1, bg="#ffffff", relief="groove", show='*')

    change_password_new_password_label = Label(hospital_change_password_container, bg="#e0e0e0", text="New Password",
                                               font=("calibri", 14))
    change_password_new_password_entry = Entry(hospital_change_password_container, width=30, show='*',
                                               font=("calibri", 16), bd=1, bg="#f9f9f9", relief="groove")

    change_password_repeated_new_password_label = Label(hospital_change_password_container, bg="#e0e0e0",
                                                        text="Repeat New Password", font=("calibri", 14))
    change_password_repeated_new_password_entry = Entry(hospital_change_password_container, width=30, show='*',
                                                        font=("calibri", 16), bd=1, bg="#f9f9f9", relief="groove")

    password_update_button = Button(hospital_change_password_container, text="Update", width=15, height=2,
                                    command=handle_hospital_change_password, bd=1)

    # Pack items
    change_password_old_password_label.pack(padx=10, pady=2)
    change_password_old_password_entry.pack(padx=30, pady=2)

    Label(hospital_change_password_container,
          bg="#e0e0e0").pack(padx=10, pady=4)

    change_password_new_password_label.pack(padx=10, pady=2)
    change_password_new_password_entry.pack(padx=30, pady=2)

    Label(hospital_change_password_container,
          bg="#e0e0e0").pack(padx=10, pady=4)

    change_password_repeated_new_password_label.pack(padx=10, pady=2)
    change_password_repeated_new_password_entry.pack(padx=30, pady=2)

    Label(hospital_change_password_container,
          bg="#e0e0e0").pack(padx=10, pady=5)

    password_update_button.pack(padx=10, pady=2)

    Label(hospital_change_password_container,
          bg="#e0e0e0").pack(padx=10, pady=15)

    hospital_change_password_container.pack(pady=80)

    hospital_change_password_frame.pack()


'''
-------------------------------------------------------------------------------------------------------
                                        PUBLIC SECTION
-------------------------------------------------------------------------------------------------------
'''


# function to create public frame
def public():
    global public_frame
    # Public Frame

    public_frame = Frame(root, bg="black", width=800, height=600)
    public_frame.pack_propagate(0)

    display_header("Public", "Back", "#00A439", 231,
                   public_frame, main_options)

    main_query = "select government.government_name, government.state_id," \
                 "sum(hospitals.positive_count), sum(hospitals.negative_count), sum(hospitals.dead_count), " \
                 "sum(hospitals.home_quarantine_count), sum(hospitals.total_patient_admitted_count) from government " \
                 "inner join hospitals on government.state_id = hospitals.state_id group by state_id order by state_id;"
    cursor.execute(main_query)
    main_result = cursor.fetchall()

    print(main_result)

    display_statistics_table_frame = Frame(
        public_frame, width=800)

    hospital_table = ttk.Treeview(display_statistics_table_frame,
                                  columns=(1, 2, 3, 4, 5, 6, 7, 8), show="headings",
                                  height=30, )

    vsb = ttk.Scrollbar(display_statistics_table_frame,
                        orient="vertical", command=hospital_table.yview)
    vsb.pack(side=RIGHT, fill=Y)

    hsb = ttk.Scrollbar(display_statistics_table_frame,
                        orient="horizontal", command=hospital_table.xview)
    hsb.pack(side=BOTTOM, fill=X)

    hospital_table.configure(yscrollcommand=vsb.set)
    hospital_table.configure(xscrollcommand=hsb.set)

    hospital_table.column("1", width=50)
    hospital_table.column("2", width=100)
    hospital_table.column("3", width=180)
    hospital_table.column("4", width=50)
    hospital_table.column("5", width=180)
    hospital_table.column("6", width=100)
    hospital_table.column("7", width=100)
    hospital_table.column("8", width=100)

    hospital_table.heading("1", text="Sr.No")
    hospital_table.heading("2", text="Government Id")
    hospital_table.heading("3", text="Government")
    hospital_table.heading("4", text="Positive Count")
    hospital_table.heading("5", text="Negative Count")
    hospital_table.heading("6", text="Dead Count")
    hospital_table.heading("7", text="Home Quarantine Count")
    hospital_table.heading("8", text="Patient Admitted Count")

    i = 1
    for item in main_result:
        columns_heading = ["" + str(i)] + list(item)
        hospital_table.insert('', 'end', values=columns_heading)
        i = i + 1

    hospital_table.pack(side=LEFT, fill=X, expand=True)

    display_statistics_table_frame.pack()

    public_frame.pack()


# calling homepage function to display
homepage()

root.mainloop()
