import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv


url = "https://www.presidency.ucsb.edu/documents/app-categories/presidential/spoken-addresses-and-remarks"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
speeches = soup.find_all("div", class_="field-title")

speechdata = []

startpg = 1
endpg = 3188

csv_file_exists = os.path.isfile('speeches_metadata.csv')

if csv_file_exists:
    with open('speeches_metadata.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  
        metadata = list(reader)

for pagenum in range(startpg, endpg + 1):
    url = f"https://www.presidency.ucsb.edu/documents/app-categories/presidential/spoken-addresses-and-remarks?page={pagenum}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    speeches = soup.find_all("div", class_="field-title")
    for index, s in enumerate(speeches, start=1):
        hrefs = []
        for a_tag in s.find_all('a'):
            hrefs.append("https://www.presidency.ucsb.edu" + a_tag['href'])
        for href in hrefs:
            response2 = requests.get(href)
            speech_soup = BeautifulSoup(response2.content, "html.parser")
            speech_text = speech_soup.find("div", class_="field-docs-content").text.strip()
            filename = f"speech_{index}_page_{pagenum}.txt"
            date_element = speech_soup.find("span", class_="date-display-single")
            date = date_element.text.strip() if date_element else "" 
            president_element = speech_soup.find("div", class_="field-title")
            president = president_element.text.strip() if president_element else ""
            title_element = speech_soup.find("div", class_="field-ds-doc-title")
            title = title_element.text.strip() if title_element else ""
            soup2 = BeautifulSoup(response2.content,"html.parser")
            cat = []
            cats = soup2.find_all("a", attrs={"typeof": "skos:Concept"})
            for c in cats:
                cat.append(c.text)
            speechdata.append([filename, date, president, title, cat, href])
            print(f"speech_{index}_page_{pagenum}")

header = ["Filename", "Date", "President", "Title", "Categories & Attributes", "URL"]
mode = 'a' if csv_file_exists else 'w'
with open('speeches_metadata.csv', mode, newline='') as f:
    writer = csv.writer(f)
    if mode == 'w':
        writer.writerow(header)  
    writer.writerows(speechdata)

