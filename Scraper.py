import requests 
from bs4 import BeautifulSoup
import csv 
from selenium import webdriver
import time
import sys
import argparse



pathToReviews = "TripReviews.csv"
pathToStoreInfo = "TripStoresInfo.csv"

#webDriver init


def scrapeRestaurantsUrls(tripURLs):
    urls =[]
    for url in tripURLs:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        results = soup.find('div', class_='_1kXteagE')
        stores = results.find_all('div', class_='wQjYiB7z')
        for store in stores:
            unModifiedUrl = str(store.find('a', href=True)['href'])
            urls.append('https://www.tripadvisor.com'+unModifiedUrl)            
    return urls

def scrapeRestaurantInfo(url):
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    storeName = soup.find('h1', class_='_3a1XQ88S').text
    avgRating = soup.find('span', class_='r2Cf69qf').text.strip()
    storeAddress = soup.find('div', class_= '_2vbD36Hr _36TL14Jn').find('span', class_='_2saB_OSe').text.strip()
    noReviews = soup.find('a', class_='_10Iv7dOs').text.strip().split()[0]
    with open(pathToStoreInfo, mode='a', encoding="utf-8") as trip:
        data_writer = csv.writer(trip, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        data_writer.writerow([storeName, storeAddress, avgRating, noReviews])

parser = argparse.ArgumentParser()
parser.add_argument('--url', required=True, help ='need starting url')
parser.add_argument('-i', '--info', action='store_true', help="Collects restaurant's info")
parser.add_argument('-m', '--many', action='store_true', help="Collects whole area info")
args = parser.parse_args()
startingUrl = args.url 
if args.info:
    info = True
else:
    info = False
if args.many:
    urls = scrapeRestaurantsUrls([startingUrl])
else:
    urls = [startingUrl]

driver = webdriver.Chrome('chromedriver.exe')
for url in urls:
    print(url)
    #if you want to scrape restaurants info
    if info == True:
        scrapeRestaurantInfo(url)

    nextPage = True
    while nextPage:
        #Requests
        driver.get(url)
        time.sleep(1)
        #Click More button
        more = driver.find_elements_by_xpath("//span[contains(text(),'More')]")
        for x in range(0,len(more)):
            try:
                driver.execute_script("arguments[0].click();", more[x])
                time.sleep(3)
            except:
                pass
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        #Store name
        storeName = soup.find('h1', class_='_3a1XQ88S').text
        #Reviews
        results = soup.find('div', class_='listContainer hide-more-mobile')
        try:
            reviews = results.find_all('div', class_='prw_rup prw_reviews_review_resp')
        except Exception:
            continue
        #Export to csv
        try:
            with open(pathToReviews, mode='a', encoding="utf-8") as trip_data:
                data_writer = csv.writer(trip_data, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
                for review in reviews:
                    ratingDate = review.find('span', class_='ratingDate').get('title')
                    text_review = review.find('p', class_='partial_entry')
                    if len(text_review.contents) > 2:
                        reviewText = str(text_review.contents[0][:-3]) + ' ' + str(text_review.contents[1].text)
                    else:
                        reviewText = text_review.text
                    reviewerUsername = review.find('div', class_='info_text pointer_cursor')
                    reviewerUsername = reviewerUsername.select('div > div')[0].get_text(strip=True)
                    rating = review.find('div', class_='ui_column is-9').findChildren('span')
                    rating = str(rating[0]).split('_')[3].split('0')[0]
                    data_writer.writerow([storeName, reviewerUsername, ratingDate, reviewText, rating])
        except:
            pass
        #Go to next page if exists
        try:
            unModifiedUrl = str(soup.find('a', class_ = 'nav next ui_button primary',href=True)['href'])
            url = 'https://www.tripadvisor.com' + unModifiedUrl
        except:
            nextPage = False




