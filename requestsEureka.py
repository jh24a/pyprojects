import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize 


#create response object as r
r = requests.get("https://eureka.utexas.edu/search/projects")

#get html text
html_doc = r.text

#running the html doc through beatiful soup gives us a
#beautiful soup object, which represents the document
# as a nested data structure (what is a nested data structure)
# --- I dont know why we have to put 'html.parser' - TODO: lookup nested data structure and parser options)
soup = BeautifulSoup(html_doc, 'html.parser') 

#organize text to make it easy to read:
# pretty_soup = soup.prettify() 
# print(pretty_soup)

#class_ = glyphicon glyphicon-exclamation-sign


#find div that is part of class "view-content", aka main content
#one way of doing it below
#content_html = soup.find_all("div", class_="view-content", limit=1)[0]
#right way of doing it below
content_html = soup.find(class_="view-content")

#break content into items
projects_html_list = content_html.find_all("div", class_="views-row")

keywords = ["app", "application", "VR", "framework", "frameworks", 
            "web scraping", "arduino", "computer vision", "computational", 
            "python", "c++", "coding", "computing", "cybersecurity", "linux", 
            "software development","software engineering", "programming", 
            "machine learning", "networking", "neural", "networks", "raspberry pi",
            "robot", "math", "mathematics", "computation", "robotics", "engineering", 
            "electronics", "mathematical", "AI", "javascript"]

unwanted = ["Border Circuits: Latina/o/e Digital Labor since 1965", "Project LEAP",
            "Cool Texas fishes in need of further research"]

def tags_match(keywords: list[str], text: list[str]) -> bool: 
    for phrase in text:
        for word in keywords:
            if word in phrase:
                return True
            
    return False

def main():    
    valid_projects = []
    no_tag_projects = []
    for project in projects_html_list:
        project_flag = True
        if project.find(class_="glyphicon glyphicon-exclamation-sign"):
            project_flag = False
        
        tags_container = project.find(class_="views-field views-field-field-project-tags")
    
        if tags_container:
            tags_box = tags_container.find(class_="field-content")
    
            text = []
            for tag in tags_box:
                if tag.get_text() != ", ":
                    text.append(tag.get_text())
                
            if tags_match(keywords, text) and project_flag:
                valid_projects.append(project)
    
        else:
            if project_flag:
                no_tag_projects.append(project)
    
    
    for project in valid_projects:                  #look at a project in list
    
        project_title = project.find(class_="field-content views-field-title")  #locate the link in title 
        a_tag = project_title.find('a',href = True)
    
        for tag in project:                         #look at the html tags in the project
            if tag.find(class_="bookmark-link"):    #if tag is the bookmark tag then ignore it
                pass
            else:
                print(tag.get_text())               #print all other tags
        print("https://eureka.utexas.edu" + a_tag['href'])  #print link to full post
        print("###################################################################################################################")
    
        print()
        print()
    print("Valid Projects: ", len(valid_projects))
    
    
    show_notags = False
    counter = 0
    if show_notags:
        print()
        print("###############################################################")
        print("PROJECTS WITH NO TAGS:")
        print("###############################################################")
        print()
        for project in no_tag_projects:
    
            project_main_content = project.find(class_ ="views-field views-field-body")
            body = word_tokenize(project_main_content.find(class_="field-content").get_text())
    
            project_title = project.find(class_="field-content views-field-title")
            a_tag = project_title.find('a',href = True)
            title = word_tokenize(project_title.get_text())
            
            if tags_match(keywords, body) or tags_match(keywords, title):
                counter = counter + 1
                print(title)
                print(body)
                for tag in project:
                    if tag.find(class_="bookmark-link"):
                        pass
                    else:
                        print(tag.get_text())
                print("https://eureka.utexas.edu" + a_tag['href'])
                print("###################################################################################################################")
    
            print()
            print()
    print("No tag projects: ", len(no_tag_projects), "-> ", counter)
    

main()

