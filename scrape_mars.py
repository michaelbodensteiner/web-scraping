from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data = {}

#########################################

# MARS NEWS #
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title=soup.find('section', class_='image_and_description_container').find('div', class_='content_title').text
    news_p=soup.find('section', class_='image_and_description_container').find('div', class_ ='article_teaser_body').text
    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p

#########################################

# FEATURED IMAGE #
    #url = 'https://spaceimages-mars.com/'
    #browser.visit(url)
    #html = browser.html
    #soup = bs(html, 'html.parser')
    featured_image_url = 'https://spaceimages-mars.com/image/featured/mars3.jpg'
    mars_data['featured_image_url'] = featured_image_url

#########################################

# MARS FACTS #
    url = 'https://galaxyfacts-mars.com'
    browser.visit(url)
    df = pd.read_html(url)
    df = df[0]
    df.columns = ['Mars - Earth Comparison', 'Mars', 'Earth']
    df = df.drop([0])
    mars_facts_table = df.to_html(classes="table table-striped", index=False) 
    mars_data['mars_facts_table'] = mars_facts_table

#########################################

# Mars Hemispheres #
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')
    
    hemisphere_image_urls = []

    descriptions = soup.find_all('h3', limit=4)

    for title in descriptions:

        browser.links.find_by_partial_text(title.text).click()
        html = browser.html
        soup = bs(html, 'html.parser')
        downloads = soup.find('div', class_='downloads')
        img_list = downloads.find('li')
        img_url = img_list.a['href']
        img_url = url + img_url
    
        dictionary = {
            "title": title.text,
            "img_url": img_url
            }
        
        hemisphere_image_urls.append(dictionary) 

        browser.back()

        print(hemisphere_image_urls)

    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    
    browser.quit()

    return mars_data