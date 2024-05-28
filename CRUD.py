from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from random import randint, randrange
import tkinter.ttk as ttk
import datetime



import sqlite3

#Make the Main Window
window = Tk()

#Set the Geometry
window.geometry("400x400")
window.title("Patient Check in")

path="C:/Users/frank/OneDrive/Desktop/CISP71_Tkinter_SQLite_Examples/"

#Adding Patient Notes feature
conn_notes = sqlite3.connect(path+ "notes.db")
c_notes = conn_notes.cursor()

#Creating the table to store the notes


c_notes.execute('''
CREATE TABLE IF NOT EXISTS patient_notes (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    date TEXT,
    notes TEXT
);
''')

#Function to add a note for a patient



#Adding a Search Patient Feature

class InputDialog(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Enter Patient Details")
        
        self.result = None
        
        Label(self, text="Last Name:").grid(row=0, column=0)
        self.last_name_entry = Entry(self)
        self.last_name_entry.grid(row=0, column=1)
        
        Label(self, text="DOB MM/DD/YYYY: " ).grid(row=1, column=0)
        self.dob_entry = Entry(self)
        self.dob_entry.grid(row=1, column=1)
        
        Button(self, text="Submit", command=self.on_submit).grid(row=2, column=0, columnspan=2)

    
    def on_submit(self):
        last_name = self.last_name_entry.get()
        dob = self.dob_entry.get()
        
        if last_name and dob:
            self.result = last_name, dob
            self.destroy()
        else:
            messagebox.showwarning("Input Error", "Please enter boith last name and date of birth")
     
def search_patient():
    dialog = InputDialog(window)
    window.wait_window(dialog)
    
    if dialog.result:
        last_name, dob = dialog.result
        conn = sqlite3.connect(path+"patientDatabase.db")
        c = conn.cursor()
        query = "SELECT * FROM patients WHERE lastName = ? AND DOB = ?"
        c.execute(query, (last_name, dob))
        result = c.fetchone()
        conn.close()
        
        if result:
            clearFields()
            pateintFirstNameEn.insert(0, result[0])
            patientLastNameEn.insert(0, result[1])
            patientDOBen.insert(0, result[2])
            patientCityEn.insert(0, result[3])
            selected.set(result[4])
            patientZipCodeEn.insert(0, result[5])
        else:
            messagebox.showinfo("Info", "No patient found with the given last name and date of birth")
#---------------------------------------------------


#TODO Add functions here but assign the command for the buttons and stuff 
def display_message_box(text):
    messagebox.showinfo("Info:", text)


def addrecord_and_update_TreeView():
    addRecord()
    displayRecords()

def clearFields():
    patientsIDEn.delete(0, END)
    pateintFirstNameEn.delete(0,END)
    patientLastNameEn.delete(0, END)
    patientDOBen.delete(0, END)
    patientCityEn.delete(0, END)
    patientZipCodeEn.delete(0, END)
    
#add function to add record and display the records
    #connect to a database if not found it will create one
    #use this placeholder variales and and a dictionary
    #Make sure to use the try catch as if this fails itll crash the whole program
def addRecord():
    #Connect to database
    #use placeholder variablesx and a dictonmamry
    conn = sqlite3.connect(path+"patientDatabase.db")
    try:
        patient_id = randrange(100,999)
        c = conn.cursor()
        c.execute("insert into patients values (?,?,?,?,?,?,?)",(
            int(patient_id),
            pateintFirstNameEn.get(),patientLastNameEn.get(),patientDOBen.get(),
            patientCityEn.get(), selected.get(), int(patientZipCodeEn.get())
        ))
        conn.commit()
        print("One record of patient added successfully")
    except:
        display_message_box("Error Something Wrong with connecting to database")
        print("Error Something Wrong with connecting to database")
    conn.close()
    clearFields()

def displayRecords():
    #tvPatient.dekete(*window.tvPatient.get_children()) # clears the treeview tvPatient
    
    #loop over the children of the treeview Patient object
    
    for row in tvPatient.get_children():
        tvPatient.delete(row)
    
    conn = sqlite3.connect(path+"patientDatabase.db")
    c = conn.cursor()
    c.execute("select *,oid from patients")
    rows = c.fetchall()
    
    for row in rows:
        patientId = row[0]
        First_Name = row[1]
        Last_Name = row[2]
        Address = row[3]
        City = row[4]
        State = row[5]
        ZipCode = row[6]
        tvPatient.insert("",'end', text=id, values=(patientId,First_Name,Last_Name,Address,City,
                                                    State, ZipCode, id))

def deleteRecord():
    """This Function is condigent that the last name field has something
    So to Fix this Everytime that a name is selected in the tree view object
    it will autofill everything into the entries so the deleted record comes up
    
    """
    #connect to the database
    #use placeholder variables and a dictionary
    conn = sqlite3.connect((path+"patientDatabase.db"))
    #This is the code we will send to the database
    qry="DELETE from patients where lastName = ?;"
    
    try:
        c = conn.cursor()
        c.execute(qry, (patientLastNameEn.get(),))
        conn.commit()
        print("record deleted successfully")
    except:
        print("Error in deleting record")
        conn.rollback()
    conn.close()
    clearFields()

def delete_then_display():
    deleteRecord()
    displayRecords()
    
def show_selected_record(event):
    clearFields()
    
    for selection in tvPatient.selection():
        item = tvPatient.item(selection)
        global id
        fName,lName,address,city,state,zipCode = item["values"][0:6]
        pateintFirstNameEn.insert(0,fName)
        patientLastNameEn.insert(0,lName)
        patientDOBen.insert(0,address)
        patientCityEn.insert(0, city)
        stateOp.setvar(state)
        patientZipCodeEn.insert(0,zipCode)
    return id    
def todo_add_function():
    return "Add Function"


#Create the List of States
stateList=["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY" ]

#Assign the return type of the selected state type since its letters its a String
selected = StringVar()

#to set the default value you can you use the .set on the selected

selected.set(stateList[4])

#Space for the labels Havent Placed them yet will do them later
patientIDLb = Label(window, text="Patients ID")
patientFirstNameLb = Label(window, text="Patient First Name")
patientLastNameLb = Label(window, text="Patients Last Name")
patientDOBLb = Label(window, text="DOB MM/DD/YYYY")
patientCityLb = Label(window, text="City")
patientStateLb = Label(window,text="State")
patientZipCodeLb = Label(window, text="Zip Code")
#-------------------------

#Now make the entry widgets for the labels 
patientsIDEn = Entry(window)
pateintFirstNameEn = Entry(window)
patientLastNameEn = Entry(window)
patientDOBen = Entry(window)
patientCityEn = Entry(window)
patientZipCodeEn = Entry(window)
#---------------------------------------------------------

#This is where Ill make the OptionMenu Widget for the drop list
#*stateList is to unpack the whole list that we declared which is the list of states

stateOp = OptionMenu(window, selected, *stateList)

#Buttton Widgets Creation 

addbtn = Button(window, text="Add Record", command=addrecord_and_update_TreeView)

displaybtn = Button(window, text="Display Records", command= displayRecords)
deletebtn = Button(window, text="Delete Record", command=delete_then_display)
updatebtn = Button(window, text="Update Patient", command=todo_add_function())

findPatient = Button(window,text="Find Patient", command=search_patient)

#Now we place Labels
patientFirstNameLb.grid(row=0,column=0)
patientLastNameLb.grid(row=1,column=0)
patientDOBLb.grid(row=2,column=0)
patientCityLb.grid(row=3, column=0)
patientStateLb.grid(row=4,column=0)
patientZipCodeLb.grid(row=5,column=0)
#Now Placing the Entries and other stuffs
pateintFirstNameEn.grid(row=0,column=1)
patientLastNameEn.grid(row=1,column=1)
patientDOBen.grid(row=2,column=1)
patientCityEn.grid(row=3,column=1)
#OptionList
stateOp.grid(row=4,column=1)
#OptionList
patientZipCodeEn.grid(row=5,column=1)


#Specify where I want the Buttons to go
addbtn.grid(row=7,column=0)
deletebtn.grid(row=8,column=1)
updatebtn.grid(row=7,column=1)
displaybtn.grid(row=8,column=0)
findPatient.grid(row=8, column=2)
#---------------------------------------------------------
#---------------------------------------------------------

#Treeview widget
#specify a tuple columns
columns = ("#1","#2","#3","#4","#5","#6",'#7')

tvPatient = ttk.Treeview(window,show="headings", height="5", columns=columns)

#specify the heading to the corresponding headings


tvPatient.heading('#1', text="Patient ID", anchor='center')
tvPatient.column('#1',width=40, anchor='center',stretch=True)

tvPatient.heading('#2', text="First Name", anchor='center')
tvPatient.column('#2', width=40, anchor='center', stretch=True)

tvPatient.heading('#3', text="Last Name", anchor='center')
tvPatient.column('#3', width=40, anchor='center', stretch=True)

tvPatient.heading('#4', text="DOB", anchor='center')
tvPatient.column('#4', width=40, anchor='center', stretch=True)

tvPatient.heading('#5', text="City", anchor='center')
tvPatient.column('#5', width=40, anchor='center', stretch=True)

tvPatient.heading('#6', text="State", anchor='center')
tvPatient.column('#6', width=40, anchor='center', stretch=True)

tvPatient.heading('#7', text="ZipCode", anchor='center')
tvPatient.column('#7', width=40, anchor='center', stretch=True)


#Notes Tree view Object
notes_columns = ("#1", "#2","#3", "#4")
tvNotes = ttk.Treeview(window, show="headings", height="5", columns=notes_columns)

#specify the heading to the corresponding headings

tvNotes.heading('#1', text="Patient ID", anchor='center')
tvNotes.column('#1',width=40, anchor='center', stretch=True)

tvNotes.heading('#2', text="First Name", anchor='center')
tvNotes.column('#2',width=40, anchor='center', stretch=True)

tvNotes.heading('#3', text="Last Name", anchor='center')
tvNotes.column('#3',width=40, anchor='center', stretch=True)

tvNotes.heading('#4', text="Notes", anchor='center')
tvNotes.column('#4',width=40, anchor='center', stretch=True)

#----------------------------------------------

    
#Bind the tree view to the function show_selected_record
tvPatient.bind("<<TreeviewSelect>>", show_selected_record)

tvPatient.grid(row=10,column=0,columnspan=10)

#Bind the Notes Tree view to the function 

#TODO
#tvNotes.bind("<<TreeviewSelect>>", show_notes;)
tvNotes.grid(row=10, column=10, columnspan=10)


displayRecords()
mainloop()