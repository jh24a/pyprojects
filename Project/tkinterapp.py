import tkinter as tk
import datetime 
from requests_html import HTMLSession
import pandas as pd 
from pandastable import Table, TableModel

from sqlalchemy import create_engine
import tkinter.font as tkFont
from tkinter import messagebox

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

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


        LARGEFONT = ("Verdana", 25) 
        MEDIUMFONT = ("Verdana", 15) 
        SMALLFONT = ("Verdana", 10) 


        infoframe = tk.Frame(self)
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
        updatebutton.bind("<Button-1>", update)
        
class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        session = HTMLSession()
        r = session.get('https://news.google.com/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNREZqY0hsNUVnSmxiaWdBUAE?hl=en-US&gl=US&ceid=US%3Aen')

        r.html.render(sleep=1, scrolldown=5)

        articles = r.html.find('article')
        newslist = []

        titles = []
        links = []
        for item in articles:
            try:
                newsitem = item.find('h3', first=True)
                titles.append(newsitem.text)
                links.append(newsitem.absolute_links)
            except:
                pass




        MEDIUMFONT = ("Verdana", 15) 
        SMALLFONT = ("Verdana", 10) 


        infoframe = tk.Frame(self)
        infoframe.pack(expand = 'True')
        news_label = tk.Label(infoframe, text = "News", font = MEDIUMFONT)
        news_label.pack()

        ls_frame = tk.Frame(infoframe)
        ls_frame.pack(fill = 'both',expand = 'True', padx = 1)
        scrollbary = tk.Scrollbar(ls_frame)
        scrollbary.pack(side=tk.RIGHT, fill=tk.Y )
        scrollbarx = tk.Scrollbar(ls_frame)
        scrollbarx.pack(side=tk.BOTTOM, fill=tk.X )
        mylist = tk.Listbox(ls_frame, font = SMALLFONT, yscrollcommand = scrollbary.set, xscrollcommand = scrollbarx.set, width = 100, height = 100)

        for line in range(len(titles)):
            mylist.insert(tk.END, titles[line], links[line], "")

        mylist.pack(side=tk.LEFT, fill = tk.BOTH )
        scrollbary.config(command=mylist.yview )
        scrollbarx.config(command=mylist.xview )

class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        session = HTMLSession()
        r = session.get('https://www.worldometers.info/coronavirus/')

        #the table we want
        table = r.html.find('#main_table_countries_today', first= True)
        #print(table)

        #this just narrows the info that we want to get from
        table_contents = r.html.find('tbody', first= True)
        #print(table_contents)

        rows = table_contents.find('tr')
        #print(len(rows))

        tabledata = []
        rowdata = []
        for row in rows:
            cells = row.find('td')
            for cell in cells:
                rowdata.append(cell.text)
            rowdata.pop()
            rowdata.pop() # dont know what the last 3 elements mean or where they come from 
            rowdata.pop()
            tabledata.append(rowdata)
            rowdata = []


        frame_table = tk.Frame(self)
        frame_table.pack(fill = 'both', expand = 'True' , anchor = 'n')

        info = pd.DataFrame(tabledata, columns = ['#', 'Country/Other', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Total Recovered', 'Increase', 'Active Cases', 'Serious/Crititcal', 'Tot Cases/1M pop', 'Deaths/1M pop', 'Total Tests', 'Tests/1M pop', 'Population', 'Continent' ])
        pt = Table(frame_table)
        pt.updateModel((TableModel(info)))
        pt.show()

class Page4(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        
        #backgroundimage = tk.PhotoImage(file='png goes here') (if we want a background
        #backgrounlabel = tk.Label(self, image=backgroundimage)
        #backgrounlabel.place(relwidth=.75, relheight=1)
      

        #frames will keep the buttons within a certain window of the main window
        Frame = tk.Frame(self, bg='white', bd=5)
        Frame.place(relx=0.5, rely=.1, relwidth=.75, relheight=.1, anchor='n')
        #titletext = tk.Label(Frame, text="Replace Text", bg='red', width=25, height=5) (not needed?)
        button1 = tk.Button(Frame, text="COVID LINK", bg='yellow', width=25, height=5)
        button1.place(relx=.7, relheight=1, relwidth=.3)
        button2 = tk.Button(Frame, text="COVID LINK", bg="pink", width=25, height=5)


        informationframe = tk.Frame(self, bg='black', bd=5)
        informationframe.place(relx=.5, rely=.25, relwidth=.75, relheight=.6, anchor='n')
        info_label = tk.Label(informationframe, text="Info goes here", bg="pink")
        info_label.place(relwidth=1, relheight=1)


        button2.pack(side="left", fill='both')
        button1.pack(side="right", fill='both')
        #titletext.pack(side="top", fill='x')

class Page5(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        def select_contacts():
            sqlengine = create_engine('mysql+pymysql://max:1234qwer@34.66.141.173/db_max', pool_recycle=3600)
            dbconnection = sqlengine.connect()
            df = pd.read_sql("select * from contacts", dbconnection)
            return df

        def search_name():
            messagebox.showinfo("Search Bar", "You don't have any messages yet!")

        fontStyle = tkFont.Font(family="Lucinda Fax", size=10)

        messageframe = tk.Frame(self)
        messageframe.pack(side = tk.TOP)
        informationframe = tk.Frame(self, bg='pink', bd=5)
        informationframe.pack(side = tk.RIGHT, padx=2, pady=2, anchor='n' )
        buttonframe = tk.Frame(self)
        buttonframe.pack(side = tk.LEFT, anchor = 'n', padx = 2)
        frame_table = tk.Frame(informationframe)
        frame_table.pack( fill= "x")#side= tk.TOP,
        names_table = Table(frame_table, height=100)
        names_table.updateModel(TableModel(select_contacts()))
        names_table.show()
        B = tk.Button(messageframe, text ="Search: ",fg="black", bg="pink", font=fontStyle, command = search_name)
        B.pack()

        entry_search = tk.Entry(messageframe, width=20, fg="black", bg="white")
        entry_search.pack(side = tk.RIGHT)
        label_messa = tk.Label(informationframe, text="Message Box", fg="black", bg="pink", font=fontStyle)
        label_messa.pack(side = tk.TOP)
        button_drafts1 = tk.Button(buttonframe, text="Drafts ", fg="black", bg="pink", font=fontStyle)
        button_drafts1.pack(side = tk.TOP)
        button_favorites1 = tk.Button(buttonframe, text="Favorites", fg="black", bg="pink", font=fontStyle)
        button_favorites1.pack(side = tk.BOTTOM)
        button_notif1 = tk.Button(buttonframe, text="Alerts", fg="black", bg="pink", font=fontStyle)
        button_notif1.pack(side = tk.BOTTOM)
        button_send1 = tk.Button(buttonframe, text="Send", fg="black", bg="pink", font=fontStyle)
        button_send1.pack(side = tk.BOTTOM)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
        p4 = Page4(self)
        p5 = Page5(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p5.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Main", command=p1.lift)
        b2 = tk.Button(buttonframe, text="News", command=p2.lift)
        b3 = tk.Button(buttonframe, text="Stats", command=p3.lift)
        b4 = tk.Button(buttonframe, text="Social", command=p4.lift)
        b5 = tk.Button(buttonframe, text="Messages", command=p5.lift)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")
        b5.pack(side="left")

        p1.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("900x800")
    root.mainloop()