# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres" : hemisphere_images(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data
    
def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():

    # Add try/except for error handling
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns names
    df.columns=['Description', 'Mars', 'Earth']
    # Drop the row without relevant information
    df = df.drop(0)
    # Set all column names as the index for a better appearance
    #df.set_index(list(df.columns.values), inplace=True)

    return df.to_html(index = False, bold_rows = False, classes=["table-bordered", "table-striped", "table-hover"])

def hemisphere_images(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    ## Get the landing page HTML
    hemisphere_html = browser.html

    ## Parse the page HTML
    hemisphere_soup = soup(hemisphere_html,'html.parser')

    ## Get all the instances of a tags with itemlink class in the parsed HTML
    hemisphere_hrefs = hemisphere_soup.find_all('a', class_='itemLink')

    ## Extract the html relative address and join it with the site url
    hemisphere_hrefs = [url + entry['href'] for entry in hemisphere_hrefs if entry['href'].find('.html') != -1] 

    ## Remove the duplicates 
    hemisphere_urls = []
    for entry in hemisphere_hrefs:
        if entry not in hemisphere_urls:
            hemisphere_urls.append(entry)
    hemisphere_urls

    ## Loop through the URL 
    for urls in hemisphere_urls:
        browser.visit(urls)
        url_html = browser.html
        url_soup = soup(url_html,'html.parser')
        url_image_href = url_soup.select('li > a')
        url_image = url + url_image_href[0]['href']
        url_title = url_soup.find('h2',class_='title').text
        hemispheres = {
            'img_url' : url_image,
            'title' : url_title
        }
        hemisphere_image_urls.append(hemispheres)
        browser.back()
    
    # 4. Return the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls
