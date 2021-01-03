# TripAdvisor-Python-Scraper-Restaurants-2021 
An implementation on python for scraping unique Restaurants's reviews or scraping a whole geographical area's reviews from TripAdvisor

Features implemented:
1) Scrape only one restaurants's reviews and store it in csv. The feutures of each review are restaurant's name, username, review, rating 
2) Scrape a whole area like a city(all restaurants in this region)
3) Scrape basic info(Restaurant's name, Address, Average Rating, Number of reviews) of each restaurant and store it in .csv
4) The click function to open the "more" button of the reviews
5) The click function to change the page

How to use:

Directly from the terminal: 
if you want to scrape only one specific restaurant pass the argument t/T if you want to keep the restaurants info or f/F if you don't, then give the tripadvisor url page of the restaurant e.x. Python scraper.py t "https://www.tripadvisor.com/Restaurant_Review-g189484-d2590994-Reviews-Marinos_Restaurant-Corinth_Corinthia_Region_Peloponnese.html"
if you want to scrape an area then search for that area in TripAdvisor's homepage and copy the link of the area. Pass t/T or f/F for the restaurant info like before, pass the character m and then pass the previous copied link. e.x. Python scraper.py m t "https://www.tripadvisor.com/Restaurants-g189484-Corinth_Corinthia_Region_Peloponnese.html" .
You need webChromeDriver downloaded in the same folder to make it work.

If you have any feature requests, don't hesitate to contact me :)

Use at own risk, it might violate TripAdvisor policies.
