#!/usr/bin/env python
# coding: utf-8

# # Mission to Mars

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo
from flask import Flask, render_template, redirect


# In[2]:


get_ipython().system('which chromedriver')


# In[3]:


# Set up Splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# ## Nasa Mars News

# In[ ]:


# Visit URL of page to be scraped through splinter
url = 'https://mars.nasa.gov/news/'

browser.visit(url)


# In[ ]:


# Visit URL of page to be scraped through splinter
url = 'https://mars.nasa.gov/news/'

browser.visit(url)


# In[ ]:


# Create html object
html = browser.html

# Parse with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
print(soup.prettify())


# In[ ]:


# Scrape and collect the latest News Title and Paragraph Text. 
# Assign the text to variables that you can reference later.

# Alternatively: (Title is coming up wrong)
# news_title = soup.find_all('div', class_ = 'content_title')find('a').text
# news_p = soup.find('div', class_ = 'article_teaser_body').text

news_title = soup.find_all('div', class_ = 'content_title')[0].text
news_p = soup.find_all('div', class_ = 'article_teaser_body')[0].text

print("Title: ", news_title)
print("Paragraph: ", news_p)


# ## JPL Mars Space Images - Featured Image

# In[ ]:


# Visit URL of page to be scraped through splinter
jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

browser.visit(jpl_url)


# In[ ]:


#Click on the the button go to the full image
full_image = browser.find_by_id("full_image")
full_image.click()
browser.is_element_present_by_text("more info", wait_time=5)
full_size = browser.links.find_by_partial_text("more info")
full_size.click()


# In[ ]:


# Create html object
jpl_html = browser.html

# Parse with BeautifulSoup
jpl_soup = BeautifulSoup(jpl_html, 'html.parser')


# In[ ]:


#Retrieve backgroud image url from style tag/scrape url
img_url = jpl_soup.find("img", class_ = "main_image")["src"]
featured_img_url = "https://www.jpl.nasa.gov" + img_url
featured_img_url


# ## Mars Facts

# In[ ]:


#Visit the Mars Facts webpage
facts_url = "https://space-facts.com/mars/"
browser.visit(facts_url)


# In[ ]:


# Use Pandas to parse the URL
tables = pd.read_html(facts_url)
tables


# In[ ]:


#Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
facts_df = tables[0]

#Assign column names
facts_df.columns = ["Description", "Value"]

#Formatting
facts_df["Description"] = facts_df["Description"].str.replace(":", "")

facts_df


# In[ ]:


#Use Pandas to convert the data to a HTML table string
facts_html = facts_df.to_html()

print(facts_html)


# ## Mars Hemispheres

# In[9]:


# Visit url to be scraped through splinter 
hems_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hems_url)


# In[10]:


# Create HTML object & Parse with BeautifulSoup
hems_html = browser.html

hems_soup = BeautifulSoup(hems_html, "html.parser")


# In[11]:


# Create empty list for saving dictionaries title, url
hemisphere_image_urls = []

products = hems_soup.find('div', class_='result-list')

hemispheres = products.find_all('div',{'class':'item'})


# In[16]:


# Loop through to append title and url
for hems in hemispheres:
    title = hems.find("h3").text
    title = title.replace(" Enhanced", "")
    img_link = hems.find("a")["href"]
    image_url = "https://astrogeology.usgs.gov/" + img_link 
    
    browser.visit(image_url)
    hems_html = browser.html
    hems_soup = BeautifulSoup(hems_html, "html.parser")
    downloads = hems_soup.find("div", class_="downloads")
    image_url = downloads.find("a")["href"]
    hemisphere_image_urls.append({"title": title, "img_url": image_url})
    
hemisphere_image_urls


# In[19]:


for i in range(len(hemisphere_image_urls)):
    print(hemisphere_image_urls[i]['title'])
    print(hemisphere_image_urls[i]['img_url'] + '\n')


# In[ ]:




