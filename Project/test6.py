  #import what we need
from requests_html import HTMLSession
session = HTMLSession()

#use session to get the page
#r = session.get('https://news.google.com/topstories?hl=en-GB&gl=GB&ceid=GB:en')
r = session.get('https://news.google.com/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNREZqY0hsNUVnSmxiaWdBUAE?hl=en-US&gl=US&ceid=US%3Aen')


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
