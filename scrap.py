from bs4 import BeautifulSoup
import urllib2
import sqlite3
import re

conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute('''CREATE TABLE movie_table
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,movie STRING UNIQUE, rating STRING)''')

def func():
    movie_object = []
    movie_count = 0
    cut_off = 50000000
    url = "http://imdb.com/boxoffice/alltimegross"
    response = urllib2.urlopen(url).read()
    soup = BeautifulSoup(response)
    main_content = soup.find("div",{"id": "main"})
    table = main_content.find("table")
    money = table.find_all(text=re.compile("^\$"))
    links = table.find_all("a")

    for i in xrange(0,len(money)):
        if movie_count < 100:
            money_val = str(money[i])
            money_val = int(money_val[1:].replace(',',''))
            if money_val >= cut_off:
                movie_count+=1;
                movie_object.append({'link': str(links[i].get('href')),
                'income': str(money[i])})
        else:
            break;

    for movie in movie_object:
        new_url = "http://imdb.com"+str(movie['link'])
        res = urllib2.urlopen(new_url).read()
        su = BeautifulSoup(res)
        title =  str(su.title.string)
        title = title[:len(title)-7]
        rating = su.find("span", {"itemprop": "ratingValue"}).text
        c.execute("INSERT or IGNORE INTO movie_table(movie,rating) VALUES (?,?);", (title,rating))
        conn.commit()
        
    c.execute("SELECT rating FROM movie_table;")
    movie_ratings = c.fetchall() 
    size = len(movie_ratings)
    sum_val = 0.0  
    for movie_rating in movie_ratings:
        sum_val += float(movie_rating[0])
    print "The average rating of 100 TOP Grossing Movies :-"
    print sum_val/size
    
if __name__ == "__main__":
    func()
