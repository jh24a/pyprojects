import tkinter as tk

import datetime 
from requests_html import HTMLSession
session = HTMLSession()

r = session.get('https://www.worldometers.info/coronavirus/')

mainInfo = r.html.find('#maincounter-wrap')

for info in mainInfo:
        titles = r.html.find('h1')
        numbers = r.html.find('.maincounter-number')

for i in range(len(titles)):
    titles[i] = titles[i].text

for j in range(len(numbers)):
    numbers[j] = numbers[j].text

def update(event):
    
    session = HTMLSession()
    r = session.get('https://www.worldometers.info/coronavirus/')

    mainInfo = r.html.find('#maincounter-wrap')

    for info in mainInfo:
            titles = r.html.find('h1')
            numbers = r.html.find('.maincounter-number')

    for i in range(len(titles)):
        titles[i] = titles[i].text

    for j in range(len(numbers)):
        numbers[j] = numbers[j].text
    
    timenumber.set(datetime.datetime.now().strftime('%c'))
    casenumber.set(numbers[0])
    deathnumber.set(numbers[1])
    reconumber.set(numbers[2])

currenttime = datetime.datetime.now().strftime('%c')


HEIGHT = 800
WIDTH = 800
root = tk.Tk()
window = tk.Canvas(root, height=HEIGHT, width=WIDTH)

window.pack()

LARGEFONT = ("Verdana", 25) 
MEDIUMFONT = ("Verdana", 15) 
SMALLFONT = ("Verdana", 10) 


infoframe = tk.Frame(root)
infoframe.place(relx=.5, rely=.25, relwidth=.75, relheight=.6, anchor='n')

timenumber = tk.StringVar()

timeframe = tk.Frame(infoframe)
timeframe.pack(pady = 6)
time_label = tk.Label(timeframe, textvariable= timenumber, font = MEDIUMFONT)
time_label.pack()
timenumber.set(currenttime)

casenumber = tk.StringVar()

casesframe = tk.Frame(infoframe)
casesframe.pack(pady = 6)
cases_title = tk.Label(casesframe, text=titles[0], font = LARGEFONT)
cases_title.pack()
cases_number = tk.Label(casesframe, textvariable=casenumber, font = MEDIUMFONT, fg = 'gray')
cases_number.pack()
casenumber.set(numbers[0])

deathnumber = tk.StringVar()

deathsframe = tk.Frame(infoframe)
deathsframe.pack(pady = 6)
deaths_title = tk.Label(deathsframe, text=titles[1], font = LARGEFONT)
deaths_title.pack()
deaths_number = tk.Label(deathsframe, textvariable=deathnumber, font = MEDIUMFONT, fg = 'red')
deaths_number.pack()
deathnumber.set(numbers[1])

reconumber = tk.StringVar()

recoframe = tk.Frame(infoframe)
recoframe.pack(pady = 6)
recovered_title = tk.Label(recoframe, text=titles[2], font = LARGEFONT)
recovered_title.pack()
recovered_number = tk.Label(recoframe, textvariable=reconumber, font = MEDIUMFONT, fg = 'green')
recovered_number.pack()
reconumber.set(numbers[2])
updatebutton = tk.Button(recoframe, text="Update")
updatebutton.pack(pady = 6)
updatebutton.bind("<Button-1>")#, update)


root.mainloop()
