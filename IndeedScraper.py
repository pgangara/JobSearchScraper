import urllib
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import time
import datetime
import re
os.chdir(r"C:\Users\pujitha.gangarapu\Documents\Projects\Scraper")




def indeed_scraper(url_template,city_list,start,max_results_per_city):

        i = 0
        results = []
        df = pd.DataFrame(columns=["Title","Location","Company","Salary", "Synopsis"])
        for city in set(city_list):
            for start in range(0, max_results_per_city, 10):
                # Grab the results from the request (as above)
                url = url_template.format(search_term,city, start)
                # Append to the full set of results
                html = requests.get(url)
                soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
                for each in soup.find_all(class_= "result" ):
                    try:
                        title = each.find(class_='jobtitle').text.replace('\n', '')
                    except:
                        title = None
                    try:
                        location = each.find('span', {'class':"location" }).text.replace('\n', '')
                    except:
                        location = None
                    try:
                        company = each.find(class_='company').text.replace('\n', '')
                    except:
                        company = None
                    try:
                        salary = each.find('span', {'class':'no-wrap'}).text
                    except:
                        salary = None
                    try:
                        synopsis = each.find(class_='summary').text.replace('\n', '').replace(',','').replace('\t','')
                        synposis = re.sub('[^A-Za-z0-9]+', '', synopsis)
                    except:
                        synopsis = None
                    try:
                        date = each.find('span',{'class':'date'}).text
                    except:
                        date = None
                    df = df.append({'Title':title, 'Location':location, 'Company':company, 'Salary':salary,'Date':date},ignore_index=True)
                    i += 1
                    if i % 100 == 0:
                        print('You have ' + str(i) + ' results. ' + str(df.dropna().drop_duplicates().shape[0]) + " of these aren't rubbish.")
        return df

if __name__ == '__main__':
    today = datetime.datetime.now().date()
    search_term = "Data+Scientist"
    city_list = ['Austin','Huston','Dallas','louisiana','St.+Louis']
    url_template = "http://www.indeed.com/jobs?q={}+%2420%2C000&l={}&start={}"
    max_results_per_city = 200
    df = indeed_scraper(url_template,city_list,0,200)
    print(today)
    filename = search_term+str(today)+".txt"
    df.to_csv(filename,sep = "\t")
