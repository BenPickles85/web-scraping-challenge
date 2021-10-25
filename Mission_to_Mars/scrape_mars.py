#!/usr/bin/env python
# coding: utf-8


from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import time
import re

def scrape_info():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # ## NASA Mars News


    url = 'https://redplanetscience.com/'
    browser.visit(url)



    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')



    news_title = soup.find('div', class_="content_title").text
    news_text = soup.find('div', class_="article_teaser_body").text
    print(f'News Title: {news_title}')
    print(f'Paragraph Text: {news_text}')


    # ## JPL Mars Space Images - Featured Image


    url = 'https://spaceimages-mars.com/'
    browser.visit(url)


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')



    results = soup.find('a', class_='showimg fancybox-thumbs')['href']

    featured_img_url = f'https://spaceimages-mars.com/{results}'
    print(featured_img_url)


    # ## Mars Facts


    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)



    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ["Description", "Mars", "Earth"]
    df = df.set_index("Description")
    df


    html_table = df.to_html()
    html_table


    # ## Mars Hemispheres

    url = 'https://marshemispheres.com/'
    browser.visit(url)


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    results = soup.find_all('div', class_='item')

    hemispheres = []

    for result in results:
        link = result.find('a', class_='itemLink product-item')['href']
        hemispheres.append(url + link)    

    hemispheres



    hemisphere_dict = []

    for hemisphere in hemispheres:
        browser.visit(hemisphere)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        img_url = url + soup.find('img', class_="wide-image")['src']
        title = soup.find('h2').text
        
        hemisphere_dict.append({"title": title, "img_url": img_url})

    # Create dictionary of all scraped data
    mars_data = {
        "mars_news": {
            "news_title": news_title,
            "news_text": news_text,
            },
        "featured_img": featured_img_url,
        "mars_facts": html_table,
        "mars_hemispheres": hemisphere_dict
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data





