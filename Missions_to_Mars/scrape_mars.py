
# # Mission to Mars

from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

# ## Nasa Mars News

    # Visit URL of page to be scraped through splinter
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)

    # Create html object
    html = browser.html

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract most recent article title and text
    news_title = soup.find_all('div', class_ = 'content_title')[1].text
    news_p = soup.find_all('div', class_ = 'article_teaser_body')[0].text


    # ## JPL Mars Space Images - Featured Image

    # Visit URL of page to be scraped through splinter
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(1)

    #Click on the the button go to the full image
    full_image = browser.find_by_id("full_image")
    full_image.click()
    browser.is_element_present_by_text("more info")
    time.sleep(1)
    full_size = browser.links.find_by_partial_text("more info")
    full_size.click()



    # Create html object
    jpl_html = browser.html

    # Parse with BeautifulSoup
    jpl_soup = BeautifulSoup(jpl_html, 'html.parser')

    #Retrieve backgroud image url from style tag/scrape url
    img_url = jpl_soup.find("img", class_ = "main_image")["src"]
    featured_img_url = "https://www.jpl.nasa.gov" + img_url


    # ## Mars Facts

    #Visit the Mars Facts webpage
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    time.sleep(1)

    # Use Pandas to parse the URL
    tables = pd.read_html(facts_url)

    #Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    facts_df = tables[0]

    #Assign column names
    facts_df.columns = ["Description", "Value"]

    #Formatting
    facts_df["Description"] = facts_df["Description"].str.replace(":", "")

    #Use Pandas to convert the data to a HTML table string
    facts_html = facts_df.to_html()

    # ## Mars Hemispheres

    # Visit url to be scraped through splinter
    hems_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hems_url)
    time.sleep(1)

    # Create HTML object & Parse with BeautifulSoup
    hems_html = browser.html

    hems_soup = BeautifulSoup(hems_html, "html.parser")

    # Create empty list for saving dictionaries title, url
    hemisphere_image_urls = []

    products = hems_soup.find('div', class_='result-list')

    hemispheres = products.find_all('div', {'class': 'item'})

    # Loop through to append title and url
    for hems in hemispheres:
        title = hems.find("h3").text
        title = title.replace(" Enhanced", "")
        img_link = hems.find("a")["href"]
        image_url = "https://astrogeology.usgs.gov/" + img_link

        browser.visit(image_url)
        time.sleep(1)
        hems_html = browser.html
        hems_soup = BeautifulSoup(hems_html, "html.parser")
        downloads = hems_soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    # for i in range(len(results)):
    #     hemisphere={}
    #     browser.find_by_css("a.product-item h3")[i].click()
    #     image_url=browser.links.find_by_text('Sample').first['href']
    #     title=browser.find_by_css("h2.title").text
    #     hemisphere["img_url"]=image_url
    #     hemisphere["title"]=title
    #     hem_image_urls.append(hemisphere)
    #     browser.back()


    # hem_image_urls


# # Store data in a dictionary
#     mars_data = {
#         "hem_image_urls": hem_image_urls,
#         "mars_fact": mars_facts,
#         "full_image_url": full_image_url,
#         "news_p":news_p,
#         "news_title":news_title
#     }

    # Assigning scraped data to a page

    mars_data = {}
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p
    mars_data["featured_img_url"] = featured_img_url
    mars_data["facts_html"] = facts_html
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    # Close the browser after scraping
    browser.quit()

    return mars_data


if __name__ == "__main__":
    print(scrape_info())