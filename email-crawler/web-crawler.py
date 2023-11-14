import time

from bs4 import BeautifulSoup
import requests, json
import sys
import csv
import re
from lxml import etree as ElementTree
import csv
import operator
import re

"""
Notes 11/4/2023
Check CSRanking ./util because contains good information about getting records from dblp
May want to add something about cross referencing institutions with countries to ensure we stay in the US
"""
def filter_america(author_list):
    us_schools = csv.reader(open("us_universities.csv", "r"), delimiter=",")
    us_schools_list = []
    updated_author_list = []
    for row in us_schools:
        us_schools_list.append(row[0])

    for item in author_list:
        if item[1] in us_schools_list:
            updated_author_list.append(item)
    return updated_author_list


def run_scraper():
    file_name = 'csrankings-a'
    output_file = file_name + '_emails.csv'
    csv_file = csv.reader(open(file_name + '.csv', "r", encoding="utf-8"), delimiter=",")
    csv.writer(open(output_file, "w")).writerow(['site title', 'email found'])

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    author_list = []
    for row in csv_file:
        #print(row[0])
        #print(row[1])
        author_list.append([row[0], row[1]])

    updated_author_list = filter_america(author_list)
    #time.sleep(5)
    print(len(author_list))
    print(len(updated_author_list))
    for item in updated_author_list:
        search_term = item[0] + ' ' + item[1]
        search_term = re.sub(r"[^\w\s]", '', search_term)
        search_term = re.sub(r"\s+", '+', search_term)
        print(search_term)
        goog_search = \
            "https://www.google.com/search?q=" \
            + search_term
        response = requests.get(goog_search, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        allData = soup.find_all("div", {"class": "g"})

        g = 0
        Data = []
        l = {}
        for i in range(0, len(allData)):
            link = allData[i].find('a').get('href')

            if link is not None:
                if link.find('https') != -1 and link.find('http') == 0 and link.find('aclk') == -1:
                    g = g + 1
                    l["link"] = link
                    try:
                        l["title"] = allData[i].find('h3').text
                    except:
                        l["title"] = None

                    try:
                        l["description"] = allData[i].find("span", {"class": "aCOpRe"}).text
                    except:
                        l["description"] = None

                    l["position"] = g

                    Data.append(l)

                    l = {}

                else:
                    continue

            else:
                continue
        print(Data)

        for item1 in Data:
            try:
                response = requests.get(item1['link'])
            except:
                print("Some error occurred")
            if response.status_code == 200:
                # Parse the content using BeautifulSoup

                soup = BeautifulSoup(response.content, "html.parser")

                links = soup.find_all('a')

                if links:
                    for i in links:
                        if 'mailto' in str(i):  # if mailto is seen anywhere in the link
                            print(i['href'][7:])  # Cuts out the 'mailto:' part
                            file = open(output_file, "a")
                            csv.writer(file).writerow([item[0], i['href'][7:]])
                            file.close()

                            break  # Only one email from each page
                    break
                else:
                    print("No mailto links found on the webpage.")
            else:
                print(f"Failed to fetch content from {item1['link']}")


run_scraper()

