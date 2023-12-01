import os
import sys
from time import sleep

import bs4
import requests

ab = 1
dentist_file = open("dentist.txt", "w")
dentist_file.write("Dentist Registar\n\n\n")
dentist_file.close()
city_and_state = []
url = "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"
dentist_name = []
dentist_number = []
dentist_activity = []
page_number = []

r = requests.get(url)

soup = bs4.BeautifulSoup(r.text, "html.parser")
states = soup.find_all("p")
states1 = soup.find_all(name="table")
bill = bs4.BeautifulSoup('<td align="left"><a href="/wiki/Renton,_Washington" title="Renton, Washington">Renton</a>',
                         "html.parser")

for tr in soup.find_all('tr'):
    for td in tr.find_all('td'):
        for li in td.find_all('li'):
            for a in li.find_all('a'):
                if len(str(a.get('title'))) < 20:
                    if "," in str(a.get('title')):
                        city_and_state.append(f"{str(a.get('title'))}")
                ab += 1
                if '(None)' in city_and_state:
                    city_and_state.remove("(None)")
print(city_and_state)
print("-------" * 20)
for element in city_and_state:
    sys.stdout = open("dentist.txt", "a")
    print(element)

    url2 = f'https://www.yellowpages.com/{element}/dentists'
    dentist_request = requests.get(url2)
    soup2 = bs4.BeautifulSoup(dentist_request.text, 'html.parser')
    for div in soup2.find_all('div', class_='pagination'):
        for li in div.find_all_next('li'):
            if str(li.text).isalnum():
                if str(li.text) != 'Next':
                    page_number.append(li.text)
    #print(page_number)
    for number in page_number:
        url2 = f"https://www.yellowpages.com/{element}/dentists?page={number}"
        soup2 = bs4.BeautifulSoup(dentist_request.text, 'html.parser')
        name = soup2.find_all('div', class_='phones phone primary')
        d_name = soup2.find_all('a', class_='business-name')
        open_status = soup2.find_all('div', class_='open-status')
        page_len = soup2.find_all('div', class_='pagination')
        #print(url2)
        for open_or_closed in open_status:
            dentist_activity.append(open_or_closed.text)
        for names in d_name:
            dentist_name.append(names.text)
        for e in name:
            dentist_number.append(e.text)
    new_list = set(zip(dentist_name[1:], dentist_number, dentist_activity))
    #print(new_list)
    for x, y, z in new_list:
        if 'OPEN NOW' in z:
            print("Dentist name: " + x, "|  Dentist Number:" + y, "   "+z)
    new_list.clear()
    dentist_activity.clear()
    dentist_number.clear()
    dentist_name.clear()
    #print(new_list)
    sleep(5)
    page_number.clear()
sys.stdout.close()
