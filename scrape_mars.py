# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

def scrape():
    # Get top Mars news story headline and paragraph
    mep_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(mep_url)
    soup = bs(response.text)
    news_title = soup.find(class_ = 'content_title').text.strip()
    news_p = soup.find(class_ = 'rollover_description_inner').text.strip()

    # Get JPL featured Mars image using Splinter and Beautiful Soup
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.is_element_visible(browser.find_link_by_partial_text, 'more info')
    browser.click_link_by_partial_text('more info')
    soup = bs(browser.html, 'html.parser')
    featured_image_url = 'https://www.jpl.nasa.gov' + soup.find(class_ = 'main_image')['src']

    # Get latest Mars weather tweet
    twt_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twt_url)
    soup = bs(browser.html, 'html.parser')
    mars_weather = soup.find(class_ = 'tweet-text').text

    # Get Mars space facts
    sf_url = 'https://space-facts.com/mars/'
    mars_df = pd.read_html(sf_url)[0]
    mars_df.columns = ['description','value']
    mars_df.set_index('description', inplace = True)
    mars_html = mars_df.to_html(classes=['table', 'table-striped', 'table-hover'])

    # Get high resolution images of Mars's hemispheres
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)
    hemisphere_image_urls = []
    links = [item['href'] for item in browser.find_link_by_partial_text('Hemisphere Enhanced')]

    for link in links:
        browser.visit(link)
        url_dict = {}
        soup = bs(browser.html, 'html.parser')
        url_dict['title'] = soup.find('h2',class_='title').text
        url_dict['img_url'] = 'https://astrogeology.usgs.gov' + soup.find('img',class_='wide-image')['src']
        hemisphere_image_urls.append(url_dict)
    
    output_dict = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'mars_html': mars_html,
        'hemisphere_image_urls': hemisphere_image_urls
    }

    return output_dict