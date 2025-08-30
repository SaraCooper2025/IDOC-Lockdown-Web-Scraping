## import modules
import pandas as pd
from playwright.async_api import async_playwright
import asyncio
import time
import csv
from datetime import datetime
import pytz
from datetime import timedelta
import csv
import os

## define key phrases to search for on IDOC webpages -- this distinguishes between full and partial lockdowns
key_phrase1 = "No visits"
key_phrase2 = "limited visits"

## define time parameters -- set everything to EST because of shift timing (see below)
est_timezone = pytz.timezone('US/Eastern')
now_est = datetime.now(est_timezone)
current_time = now_est.time()
current_date = now_est.date()
current_hour = datetime.now(est_timezone).hour
yesterday_date = (current_date)-timedelta(days=1)
current_date_str = str(current_date)
current_hour_str = str(current_hour)

## IDOC shifts are 11pm-7am, 7am-3pm, 3pm-11pm -- timezone is set to EST so that all shifts fall within a single day 
if now_est.hour >= 0 or now_est.hour < 8:
    shift = 'Shift 1'
elif now_est.hour >= 8 and now_est.hour < 14:
    shift = 'Shift 2'
else:
    shift = 'Shift 3'

## this is the master list of IDOC facility lockdown pages
urls = [
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.big-muddy-river-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.centralia-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.danville-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.decatur-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.dixon-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.east-moline-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.graham-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.hill-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.illinois-river-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.jacksonville-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.lawrence-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.lincoln-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.logan-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.menard-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.pinckneyville-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.joliet-treatment-center.html"
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.pontiac-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.robinson-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.shawnee-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.sheridan-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.southwestern-illinois-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.stateville-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.taylorville-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.vandalia-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.vienna-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.western-illinois-correctional-center.html"
]

## a smaller selection of IDOC facilities to test this script, can also be substituted if interested only in specific facilities
sites = [
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.graham-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.centralia-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.lawrence-correctional-center.html",
]

## dynamic web scrapper function
async def main():
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        for url in urls:
            try:
                ## load page and wait 2 seconds so that all content loads
                await page.goto(url)
                time.sleep(2)
                content = await page.content()
                ## search for key phrases to identify full or partial lockdown
                full_lockdown = int(key_phrase1.lower() in content.lower())
                partial_lockdown = int(key_phrase2.lower()in content.lower())
                ## get the facility name from the url
                facility_name = url.split('https://idoc.illinois.gov/facilities/lockdowninformation/facility.')[1].split('.html')[0].replace('-', ' ')
                ## IDOC shifts are 11pm-7am, 7am-3pm, 3pm-11pm -- timezone is set to EST so that all shifts fall within a single day 
                if now_cst.hour >= 0 or now_cst.hour < 8:
                    shift = 'Shift 1'
                elif now_cst.hour >= 8 and now_cst.hour < 14:
                    shift = 'Shift 2'
                else:
                    shift = 'Shift 3'
                ## structure the results
                results.append({"Facility": facility_name, "Full Lockdown": full_lockdown, "Partial Lockdown": partial_lockdown, "Date": current_date, "Time": now_cst, "Shift": shift})
            except Exception as e:
                results.append({"Facility": facility_name, "Full Lockdown": False, "Partial Lockdown": False, "Date": current_date, "Time": now_cst, "Shift": shift, "Error": str(e)})
        await browser.close()
    ## load the results and return as a dataframe
    df = pd.DataFrame(results)
    return df

## set this script to create a CSV file in my repository under a /data folder and to update it with new results when script is run through GitHub Actions
lockdown_data = asyncio.run(main())

## ensure data directory exists
os.makedirs("data", exist_ok=True)

daily_scrape = "data/daily_scrape.csv"

## create new file if it does not already exist, otherwise concat results to existing file
if os.path.exists(daily_scrape):
    scrape_df = pd.read_csv(daily_scrape)
    scrape_df = pd.concat([scrape_df, lockdown_data], ignore_index=True)
else:
    scrape_df = lockdown_data

## save the updated daily_scrape.csv into the /data folder
scrape_df.to_csv(daily_scrape, index=False)


