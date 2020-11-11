{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Mission to Mars"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "from splinter import Browser\n",
    "from bs4 import BeautifulSoup\n",
    "import requests\n",
    "import pandas as pd\n",
    "import pymongo\n",
    "from flask import Flask, render_template, redirect"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "/usr/local/bin/chromedriver\r\n"
     ]
    }
   ],
   "source": [
    "!which chromedriver"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Set up Splinter\n",
    "executable_path = {'executable_path': '/usr/local/bin/chromedriver'}\n",
    "browser = Browser('chrome', **executable_path, headless=False)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Nasa Mars News"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visit URL of page to be scraped through splinter\n",
    "url = 'https://mars.nasa.gov/news/'\n",
    "\n",
    "browser.visit(url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visit URL of page to be scraped through splinter\n",
    "url = 'https://mars.nasa.gov/news/'\n",
    "\n",
    "browser.visit(url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create html object\n",
    "html = browser.html\n",
    "\n",
    "# Parse with BeautifulSoup\n",
    "soup = BeautifulSoup(html, 'html.parser')\n",
    "print(soup.prettify())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "# Scrape and collect the latest News Title and Paragraph Text. \n",
    "# Assign the text to variables that you can reference later.\n",
    "\n",
    "# Alternatively: (Title is coming up wrong)\n",
    "# news_title = soup.find_all('div', class_ = 'content_title')find('a').text\n",
    "# news_p = soup.find('div', class_ = 'article_teaser_body').text\n",
    "\n",
    "news_title = soup.find_all('div', class_ = 'content_title')[0].text\n",
    "news_p = soup.find_all('div', class_ = 'article_teaser_body')[0].text\n",
    "\n",
    "print(\"Title: \", news_title)\n",
    "print(\"Paragraph: \", news_p)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## JPL Mars Space Images - Featured Image"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visit URL of page to be scraped through splinter\n",
    "jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'\n",
    "\n",
    "browser.visit(jpl_url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Click on the the button go to the full image\n",
    "full_image = browser.find_by_id(\"full_image\")\n",
    "full_image.click()\n",
    "browser.is_element_present_by_text(\"more info\", wait_time=5)\n",
    "full_size = browser.links.find_by_partial_text(\"more info\")\n",
    "full_size.click()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create html object\n",
    "jpl_html = browser.html\n",
    "\n",
    "# Parse with BeautifulSoup\n",
    "jpl_soup = BeautifulSoup(jpl_html, 'html.parser')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Retrieve backgroud image url from style tag/scrape url\n",
    "img_url = jpl_soup.find(\"img\", class_ = \"main_image\")[\"src\"]\n",
    "featured_img_url = \"https://www.jpl.nasa.gov\" + img_url\n",
    "featured_img_url"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Mars Facts"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Visit the Mars Facts webpage\n",
    "facts_url = \"https://space-facts.com/mars/\"\n",
    "browser.visit(facts_url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Use Pandas to parse the URL\n",
    "tables = pd.read_html(facts_url)\n",
    "tables"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.\n",
    "facts_df = tables[0]\n",
    "\n",
    "#Assign column names\n",
    "facts_df.columns = [\"Description\", \"Value\"]\n",
    "\n",
    "#Formatting\n",
    "facts_df[\"Description\"] = facts_df[\"Description\"].str.replace(\":\", \"\")\n",
    "\n",
    "facts_df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Use Pandas to convert the data to a HTML table string\n",
    "facts_html = facts_df.to_html()\n",
    "\n",
    "print(facts_html)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Mars Hemispheres"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visit url to be scraped through splinter \n",
    "hems_url = \"https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars\"\n",
    "browser.visit(hems_url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create HTML object & Parse with BeautifulSoup\n",
    "hems_html = browser.html\n",
    "\n",
    "hems_soup = BeautifulSoup(hems_html, \"html.parser\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create empty list for saving dictionaries title, url\n",
    "hemisphere_image_urls = []\n",
    "\n",
    "products = hems_soup.find('div', class_='result-list')\n",
    "\n",
    "hemispheres = products.find_all('div',{'class':'item'})"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[{'title': 'Cerberus Hemisphere ',\n",
       "  'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'},\n",
       " {'title': 'Schiaparelli Hemisphere ',\n",
       "  'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'},\n",
       " {'title': 'Syrtis Major Hemisphere ',\n",
       "  'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'},\n",
       " {'title': 'Valles Marineris Hemisphere ',\n",
       "  'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'},\n",
       " {'title': 'Cerberus Hemisphere',\n",
       "  'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'},\n",
       " {'title': 'Schiaparelli Hemisphere',\n",
       "  'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'},\n",
       " {'title': 'Syrtis Major Hemisphere',\n",
       "  'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'},\n",
       " {'title': 'Valles Marineris Hemisphere',\n",
       "  'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]"
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Loop through to append title and url\n",
    "for hems in hemispheres:\n",
    "    title = hems.find(\"h3\").text\n",
    "    title = title.replace(\" Enhanced\", \"\")\n",
    "    img_link = hems.find(\"a\")[\"href\"]\n",
    "    image_url = \"https://astrogeology.usgs.gov/\" + img_link \n",
    "    \n",
    "    browser.visit(image_url)\n",
    "    hems_html = browser.html\n",
    "    hems_soup = BeautifulSoup(hems_html, \"html.parser\")\n",
    "    downloads = hems_soup.find(\"div\", class_=\"downloads\")\n",
    "    image_url = downloads.find(\"a\")[\"href\"]\n",
    "    hemisphere_image_urls.append({\"title\": title, \"img_url\": image_url})\n",
    "    \n",
    "hemisphere_image_urls"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Cerberus Hemisphere \n",
      "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg\n",
      "\n",
      "Schiaparelli Hemisphere \n",
      "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg\n",
      "\n",
      "Syrtis Major Hemisphere \n",
      "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg\n",
      "\n",
      "Valles Marineris Hemisphere \n",
      "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg\n",
      "\n",
      "Cerberus Hemisphere\n",
      "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg\n",
      "\n",
      "Schiaparelli Hemisphere\n",
      "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg\n",
      "\n",
      "Syrtis Major Hemisphere\n",
      "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg\n",
      "\n",
      "Valles Marineris Hemisphere\n",
      "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg\n",
      "\n"
     ]
    }
   ],
   "source": [
    "for i in range(len(hemisphere_image_urls)):\n",
    "    print(hemisphere_image_urls[i]['title'])\n",
    "    print(hemisphere_image_urls[i]['img_url'] + '\\n')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
