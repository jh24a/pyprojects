'''
  from datetime import date
  from bs4 import BeautifulSoup
  import requests
  #import spacy 
  import pandas as pd


  today = date.today()

  d = today.strftime("%m-%d-%y")
  #print("date =", d)

  cnn_url="https://www.cnn.com/world/live-news/coronavirus-outbreak-{}-intl-hnk/index.html".format(d)

  print(cnn_url)



  html = requests.get(cnn_url).text

  soup = BeautifulSoup(html)

  #print(soup.title)

  nlp = spacy.load('en_core_web_sm')

  for link in soup.find_all("h2"):
      
      print("Headline : {}".format(link.text))
      for ent in nlp(link.text).ents: 
        print("\tText : {}, Entity : {}".format(ent.text, ent.label_))



  nbc_url='https://www.nbcnews.com/health/coronavirus'
  cnbc_rss_url='https://www.cnbc.com/id/10000108/device/rss/rss.html'

  urls=[cnn_url, nbc_url,cnbc_rss_url]
  formats=['html.parser','html.parser','xml']
  tags=['h2','h2','description']
  website=['CNN', 'NBC','CNBC']

  crawl_len=0
  for url in urls:
      print("Crawling web page ..........{}".format(url))
      response = requests.get(url)
      soup = BeautifulSoup(response.content,formats[crawl_len])

      for link in soup.find_all(tags[crawl_len]):

        if(len(link.text.split(" ")) > 4):
          print("Headline : {}".format(link.text))

          entities=[]
          for ent in nlp(link.text).ents: 
            print("\tText : {}, Entity : {}".format(ent.text, ent.label_)) 

      crawl_len=crawl_len+1



      
  crawl_len=0
  news_dict=[]
  for url in urls:
      response = requests.get(url)
      soup = BeautifulSoup(response.content,formats[crawl_len])

      for link in soup.find_all(tags[crawl_len]):

        if(len(link.text.split(" ")) > 4):

          entities=[]

          entities=[(ent.text, ent.label_) for ent in nlp(link.text).ents]

          news_dict.append({'website':website[crawl_len],'url': url,'headline':link.text,'entities':entities})
      
      crawl_len=crawl_len+1




  


  news_df=pd.DataFrame(news_dict)

  pd.set_option('max_colwidth', 800)

  news_df.head(20)
'''
'''
  import tkinter as tk
  import pandas as pd 
  from pandastable import Table, TableModel

  #import what we need
  from requests_html import HTMLSession
  session = HTMLSession()

  #use session to get the page
  #r = session.get('https://news.google.com/topstories?hl=en-GB&gl=GB&ceid=GB:en')
  r = session.get('https://news.google.com/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNREZqY0hsNUVnSmxiaWdBUAE?hl=en-GB&gl=GB&ceid=GB%3Aen')


  #render the html, sleep=1 to give it a second to finish before moving on. scrolldown= how many times to page down on the browser, to get more results. 5 was a good number here
  r.html.render(sleep=0, scrolldown=3)

  #find all the articles by using inspect element and create blank list
  articles = r.html.find('article')
  newslist = []

  #loop through each article to find the title and link. try and except as repeated articles from other sources have different h tags.
  for item in articles:
      try:
          newsitem = item.find('h3', first=True)
          title = newsitem.text
          link = newsitem.absolute_links
          newsarticle = {
              'title': title,
              'link' : link
          }
          newslist.append(newsarticle)
      except:
        pass

  #print the length of the list
  for news in newslist:
    print(news)
    print()


  HEIGHT = 800
  WIDTH = 800
  root = tk.Tk()
  window = tk.Canvas(root, height=HEIGHT, width=WIDTH)

  window.pack()

  LARGEFONT = ("Verdana", 25) 
  MEDIUMFONT = ("Verdana", 15) 
  SMALLFONT = ("Verdana", 10) 


  infoframe = tk.Frame(root)
  infoframe.pack(expand = 'True')
  frame_table = tk.Frame(infoframe)
  frame_table.pack(fill = 'both',expand = 'True')
  info = pd.DataFrame(newslist, columns = ["title", "link"])
  pt = Table(frame_table)
  pt.updateModel((TableModel(info)))
  pt.show()


  root.mainloop() '''

import tkinter as tk
from requests_html import HTMLSession
import pandas as pd 
from pandastable import Table, TableModel

session = HTMLSession()
r = session.get('https://www.worldometers.info/coronavirus/')

#the table we want
table = r.html.find('#main_table_countries_today', first= True)
#print(table)

#this just narrows the info that we want to get from
table_contents = r.html.find('tbody', first= True)
#print(table_contents)



rows = table_contents.find('tr')
print(len(rows))

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


for i in tabledata:
  print(i)
  print()

'''
HEIGHT = 600
WIDTH = 1000

root = tk.Tk()

LARGEFONT = ("Verdana", 25) 
MEDIUMFONT = ("Verdana", 15) 
SMALLFONT = ("Verdana", 10) 



frame_table = tk.Frame(root)
frame_table.pack(fill = 'both', expand = 'True' , anchor = 'n')

info = pd.DataFrame(tabledata, columns = ['#', 'Country/Other', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Total Recovered', 'Increase', 'Active Cases', 'Serious/Crititcal', 'Tot Cases/1M pop', 'Deaths/1M pop', 'Total Tests', 'Tests/1M pop', 'Population', 'Continent' ])
pt = Table(frame_table)
pt.updateModel((TableModel(info)))
pt.show()

root.mainloop()

'''