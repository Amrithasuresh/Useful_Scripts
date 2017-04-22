from __future__ import print_function
import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd


# open the file
writefile = open('scientific_reports_analysis.txt', 'w')

# write the below string as a first line in the file
writefile.write("DOI, Date_recieved, Date_accepted, Date_published, Year, \
Time_taken_to_accept, Time_taken_to_publish, Total_time" + "\n")


# We create a function which takes the text with dates as double codes and returns dates
def double_quotes(text):
    try:
        # matches string betweent double quotes
        matches = re.findall(r'\"(.+?)\"', text)

        return matches[0],matches[1],matches[2]

    except: 
        return None

# We create a function which takes Scientific article (url) and fetches \
# "recieved date, reviewed date and online published year
# and also prints the difference in dates as date_recieved, ,date_accepted, date_publised
def fetch_publication_date(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    doi = re.search("doi:\d{2}.\d{4}\/\w+", plain_text)
    doi = doi.group(0)
    soup = BeautifulSoup(plain_text,"lxml")

    # This fetches the word "time" from "a"
    # Sample "a" variable contains below line
    # [<time datetime="2011-02-10">10 February 2011</time>,
    # <time datetime="2011-03-01">01 March 2011</time>,
    # <time datetime="2011-06-14" itemprop="datePublished">14 June 2011</time>]
    a = soup.findAll('time')

    # this calls the function "double_quotes" above
    if double_quotes(str(a)):
        date_recieved, date_accepted, date_published = double_quotes(str(a))
        year = re.findall(r'\d{4}',date_published)
        year = ','.join(year)

    try:
        # calculate the difference of date using datetime module
        t1 = datetime.strptime(date_recieved, '%Y-%m-%d')
        t2 = datetime.strptime(date_accepted, '%Y-%m-%d')
        t3 = datetime.strptime(date_published, '%Y-%m-%d')
        time_taken_to_accept = ((t2 - t1).days)
        time_taken_to_publish = ((t3 - t2).days)
        total_time = ((t3 - t1).days)

        return doi, date_recieved, date_accepted, date_published, str(year), str(time_taken_to_accept), str(
            time_taken_to_publish), str(total_time)

    except:

        return None

# fetch_publication_date eg ('http://www.nature.com/articles/srep00228')
# Scientific report article starts from 00001 to 26835 with static website as "http://www.nature.com/articles/srep"


for i in range(1, 30100, 1):
    try:
        num = "{:05d}".format(i)
        url = "http://www.nature.com/articles/srep" + str(num)
        print("Fetching the article number:\n",url)
        data = fetch_publication_date(url)
    
        if data:
            #print('{0} \n'.format(",".join(str(x) for x in data)))
            writefile.write('{0} \n'.format(",".join(str(x) for x in data)))

    except:
        pass
