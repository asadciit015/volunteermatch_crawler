[VolunteerMatch](https://www.volunteermatch.org) Crawler
=========================================================

This is a simple VolunteerMatch scraper built with [Scrapy](https://github.com/scrapy/scrapy)
and [Scrapy Cloud](https://scrapinghub.com/scrapy-cloud).

It is basically a Scrapy project with one spider for each online organization that we want to scrap  from US Regions



## Customizing the Scraper


## Installing and Running

1. Clone this repo:


2. Enter the folder and install the project dependencies:

        $ cd volunteermatch_crawler
        $ pip install -r requirements.txt

## Running in a Local Environment

You can run this project on Scrapy Cloud or on your local environment. The only dependency
from Scrapy Cloud is the [Collections API](https://doc.scrapinghub.com/api/collections.html),
but the spiders and the monitor can be executed locally.


Then run the spiders via command line:

    $ scrapy crawl organization_crawler -o name-of-csv.csv

This will run the spider named as `organization_crawler` and store the scraped data into
a Scrapy Cloud collection, under the project you set in the last step.
