########### PROJECT ###################

from pandastable import Table, TableModel
import pandas as pd
import tkinter as tk
from sqlalchemy import create_engine
import tkinter.font as tkFont
from tkinter import messagebox

#can change the size of the window through HEIGHT and WIDTH
root = tk.Tk()
informationframe = tk.Frame(root, bg='pink', bd=5)
informationframe.place(relx=.5, rely=.25, relwidth=.75, relheight=.6, anchor='n', )
frame_table = tk.Frame(informationframe)
names_table = Table(frame_table, height=100)
root.title("COVID-19 Database")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry('625x400')

def select_contacts():
    sqlengine = create_engine('mysql+pymysql://max:1234qwer@34.66.141.173/db_max', pool_recycle=3600)
    dbconnection = sqlengine.connect()
    df = pd.read_sql("select * from contacts", dbconnection)
    return df



root.title("COVID-19 Database")


fontStyle = tkFont.Font(family="Lucinda Fax", size=10)

frame_table.pack(side= tk.TOP, fill= "x")




def search_name():
    messagebox.showinfo("Search Bar", "You don't have any messages yet!")
B = tk.Button(root, text ="Search: ",fg="black", bg="pink", font=fontStyle, command = search_name)

B.pack()

entry_search = tk.Entry(width=20, fg="black", bg="white")
entry_search.place(x= 347, y= 9)
label_messa = tk.Label(text="Message Box", fg="black", bg="pink", font=fontStyle)
label_messa.place(x=74, y=75)
button_drafts1 = tk.Button(text="Drafts ", fg="black", bg="pink", font=fontStyle)
button_drafts1.place(x=10, y=165)
button_favorites1 = tk.Button(text="Favorites", fg="black", bg="pink", font=fontStyle)
button_favorites1.place(x=10, y=105)
button_notif1 = tk.Button(text="Alerts", fg="black", bg="pink", font=fontStyle)
button_notif1.place(x=10, y=135)
button_send1 = tk.Button(text="Send", fg="black", bg="pink", font=fontStyle)
button_notif1.place(x=10, y=135)


names_table.updateModel(TableModel(select_contacts()))
names_table.place(relx=.5, rely=.25, relwidth=.75, relheight=.6)
names_table.show()

root.mainloop()