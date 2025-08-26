from bs4 import BeautifulSoup
import requests
import pandas
import csv

from urllib3.filepost import writer

page_to_scrape = requests.get("https://quotes.toscrape.com")
soup = BeautifulSoup(page_to_scrape.text, "html.parser")
quotes = soup.find_all("span", attrs={"class" : "text"})
authors = soup.find_all ("small", attrs={"class" : "author"})


file = open("scraped_quotes.csv", "w")
writer = csv.writer(file)

writer.writerow(["QUOTES", "AUTHORS"])

for quote, author in zip (quotes, authors):
    print (quote.text + " - " + author.text)
    writer.writerow([quote.text, author.text])
file.close()
