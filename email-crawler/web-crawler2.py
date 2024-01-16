"""
Web Crawler 2
Authors: Aaron Ducote and Torin Perkins
"""
import ssl

from bs4 import BeautifulSoup
import requests, json
import csv
import re
from string import ascii_lowercase as alc
import time

total_requests = 0
def filter_america(author_list):
    """
    filter_america: filters university list based on list of American Universities
    :param author_list: the list of authors and their universities from given csv
    :returns updated_author_list: the filtered author list
    """
    # get list of US schools
    us_schools = csv.reader(open("us_universities.csv", "r"), delimiter=",")
    us_schools_list = []
    updated_author_list = []
    for row in us_schools:
        us_schools_list.append(row[0])
    # filter list
    for item in author_list:
        if item[1] in us_schools_list:
            updated_author_list.append(item)
    return updated_author_list


def run_scraper(file_name, usa=False):
    """
    run_scraper: scrapes the web for emails of professors given a csv of their name and association
    :return:
    """
    """"""""""""

    # -----------------------------
    # file name to read

    # -----------------------------
    if usa:
        output_file = 'emails/usa only/' + file_name + '_usa_emails.csv'
    else:
        output_file = 'emails/international/' + file_name + '_emails.csv'

    # read csv
    output_opened = open(output_file, "w")
    csv_file = csv.reader(open('names/' + file_name + '.csv', "r", encoding="utf-8"), delimiter=",")
    csv.writer(output_opened).writerow(['site title', 'email found'])
    output_opened.close()



    # create author list
    author_list = []
    for row in csv_file:
        author_list.append([filter_non_ascii(row[0]), filter_non_ascii(row[1]), filter_non_ascii(row[2])])
    # filter american schools
    if usa:
        updated_author_list = filter_america(author_list)
    else:
        updated_author_list = author_list
    print(len(updated_author_list))
    for author_info in updated_author_list:
        # create search term string
        print(author_info)

        # do google search for author
        try:
            response = requests.get(author_info[2])
        except Exception as e:
            print("exception: " + str(e))
            google_search(author_info, output_file)
            continue
        # soup = BeautifulSoup(response.text, "html.parser")

        # find mailto link for each link found
        # break on the first one

        if response.status_code == 200:
            # Parse the content using BeautifulSoup
            try:
                soup = BeautifulSoup(response.content, "html.parser")
            except Exception as e:
                print("exception: " + str(e))
                google_search(author_info, output_file)
                continue

            links = soup.find_all('a', href=lambda x: x and x.startswith('mailto:'))

            if links:
                for i in links:
                    print(i['href'][7:])  # Cuts out the 'mailto:' part
                    file = open(output_file, "a")
                    csv.writer(file).writerow([author_info[0], i['href'][7:]])
                    file.close()

                    break  # Only one email from each page
            else:
                print("No mailto links found on the webpage.")
                google_search(author_info, output_file)
        else:
            print(f"Failed to fetch content from {author_info[2]}")
            google_search(author_info, output_file)


def google_search(item, output_file):
    global total_requests
    total_requests += 1
    print("Conducting Google Search on Request: " + str(total_requests))
    search_term = item[0] + ' ' + item[1]
    search_term = re.sub(r"[^\w\s]", '', search_term)
    search_term = re.sub(r"\s+", '+', search_term)
    # headers for bs4
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    goog_search = \
        "https://www.google.com/search?q=" \
        + search_term
    # do google search for author
    response = requests.get(goog_search, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    allData = soup.find_all("div", {"class": "g"})

    g = 0
    Data = []
    l = {}
    # filter through all links found
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
    # print(Data)

    # find mailto link for each link found
    # break on the first one
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

def filter_non_ascii(input_str):
    return re.sub(r'[^\x00-\x7F]+', '', input_str)

if __name__ == "__main__":

    # for letter in alc:
        #run_scraper('csrankings-' + letter, False)
    run_scraper('csrankings-h', True)
    print(total_requests)
