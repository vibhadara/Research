import os
import requests
from bs4 import BeautifulSoup

directory = "all_speeches"
if not os.path.exists(directory):
    os.makedirs(directory)

url = "https://www.presidency.ucsb.edu/documents/app-categories/presidential/spoken-addresses-and-remarks"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

speeches = soup.find_all("div", class_="field-title")

for index, s in enumerate(speeches, start = 1):
    hrefs = []
    for a_tag in s.find_all('a'):  
        hrefs.append("https://www.presidency.ucsb.edu" + a_tag['href'])
    for href in hrefs:
        response2 = requests.get(href)
        speech_soup = BeautifulSoup(response2.content, "html.parser")
        speech_text = speech_soup.find("div", class_="field-docs-content").text.strip()
        filename = f"speech_{index}_page_0.txt"
        filepath = os.path.join(directory, filename)
        with open(filepath, "w") as file:
                file.write(speech_text)
        print(f"speech_{index}_page_0")

startpg = 1
endpg = 3189

for pagenum in range(startpg, endpg + 1):
    url = f"https://www.presidency.ucsb.edu/documents/app-categories/presidential/spoken-addresses-and-remarks?page={pagenum}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    speeches = soup.find_all("div", class_="field-title")
    for index, s in enumerate(speeches, start = 1):
        hrefs = []
        for a_tag in s.find_all('a'):  
            hrefs.append("https://www.presidency.ucsb.edu" + a_tag['href'])
        for href in hrefs:
            response2 = requests.get(href)
            speech_soup = BeautifulSoup(response2.content, "html.parser")
            speech_text = speech_soup.find("div", class_="field-docs-content").text.strip()
            filename = f"speech_{index}_page_{pagenum}.txt"
            filepath = os.path.join(directory, filename)
            with open(filepath, "w") as file:
                    file.write(speech_text)
            print(f"speech_{index}_page_{pagenum}")
   


