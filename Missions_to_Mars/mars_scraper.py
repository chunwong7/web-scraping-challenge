from bs4 import BeautifulSoup as bs
from selenium import webdriver
from splinter import Browser
import time
import pandas as pd

scraped_data = {
    'Nasa_Headlines': [],
    'Nasa_Paragraphs': [],
    'Mars_Featured_Pic': [],
    'Mars_Weather': [],
    'Mars_Facts': [],
    'Mars_Hemi_Names': [],
    'Mars_Hemi_Links': []
}
mars_invid_links = []


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    #nasa page scraper
    browser = init_browser()
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    time.sleep(5) #wait for page to load
    html = browser.html
    soup = bs(html, 'html.parser')
    data_list = soup.find('ul', class_='item_list')
    nasa_headers = data_list.find_all('div', class_='content_title')
    for items in nasa_headers:
        scraped_data['Nasa_Headlines'].append(items.text)
    nasa_para = data_list.find_all('div', class_='article_teaser_body')
    for items in nasa_para:
        scraped_data['Nasa_Paragraphs'].append(items.text)
    browser.quit()
    
    #Mars Feature picture scape
    browser = init_browser()
    mars_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_url)
    time.sleep(5)
    html2 = browser.html
    soup2 = bs(html2, 'html.parser')
    feature_div = soup2.find('div', class_='carousel_container')
    feature_image = feature_div.find('a', id='full_image')
    image_url = feature_image.get('data-fancybox-href')
    nasa_link = f"https://www.jpl.nasa.gov{image_url}"
    scraped_data['Mars_Featured_Pic'].append(nasa_link)
    browser.quit()

    #Mars Weather Scrape
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    driver = webdriver.Chrome()
    driver.get(twitter_url)
    time.sleep(10)
    firsttweet_div = driver.find_elements_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div/div/div/div/div/div[2]/section/div/div/div/div/div/div/article/div/div[2]/div[2]/div[2]/div/div/span")
    firsttweet = firsttweet_div[0].text
    scraped_data['Mars_Weather'].append(firsttweet)
    driver.close()

    #Mars Fact Scrape
    fact_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(fact_url)
    mars_facts = tables[0]
    mars_facts = mars_facts.set_index(0)
    mars_facts_dict = mars_facts.to_dict()[1]
    scraped_data['Mars_Facts'].append(mars_facts_dict)

    #Mars Hemisphere Images Scrape
    browser = init_browser()
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    time.sleep(5)
    html5 = browser.html
    soup5 = bs(html5, 'html.parser')
    hemi_links_div = soup5.find_all('div', class_='item')
    mars_page = 'https://astrogeology.usgs.gov'
    for result in hemi_links_div:
        mars_links = result.find('a', class_='itemLink').get('href')
        link_title = result.find('h3').text
        scraped_data['Mars_Hemi_Names'].append(link_title)
        mars_invid_links.append(f'{mars_page}{mars_links}')
    browser.quit()
    
    for link in mars_invid_links:
        browser = init_browser()
        browser.visit(link)
        time.sleep(2)
        html6 = browser.html
        soup6 = bs(html6, 'html.parser')
        hemi_pic_img = soup6.find('img', class_='wide-image')
        hemi_pic_link = hemi_pic_img['src']
        hemi_link = f'{mars_page}{hemi_pic_link}'
        scraped_data['Mars_Hemi_Links'].append(hemi_link)
        browser.quit()

    return scraped_data

