import pandas as pd
from playwright.async_api import async_playwright
import asyncio
import time
import csv
from datetime import datetime, date
import pytz
from datetime import timedelta
import csv
import os

key_phrase1 = "No visits"
key_phrase2 = "limited visits"
cst_timezone = pytz.timezone('US/Central')
now_cst = datetime.now(cst_timezone)
current_date = now_cst.date()
current_hour = datetime.now(cst_timezone).hour
yesterday_date = (current_date)-timedelta(days=1)
current_date_str = str(current_date)
current_hour_str = str(current_hour)

if now_cst.hour >= 23 or now_cst.hour < 7:
    shift = 'Shift 1'
elif now_cst.hour >= 7 and now_cst.hour < 15:
    shift = 'Shift 2'
else:
    shift = 'Shift 3'

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

sites = [
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.graham-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.centralia-correctional-center.html",
    "https://idoc.illinois.gov/facilities/lockdowninformation/facility.lawrence-correctional-center.html",
]

async def main():
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        for url in urls:
            try:
                await page.goto(url)
                time.sleep(2)
                content = await page.content()
                full_lockdown = int(key_phrase1.lower() in content.lower())
                partial_lockdown = int(key_phrase2.lower()in content.lower())
                facility_name = url.split('https://idoc.illinois.gov/facilities/lockdowninformation/facility.')[1].split('.html')[0].replace('-', ' ')
                if now_cst.hour >= 23 or now_cst.hour < 7:
                    shift = 'Shift 1'
                elif now_cst.hour >= 7 and now_cst.hour < 15:
                    shift = 'Shift 2'
                else:
                    shift = 'Shift 3'
                results.append({"URL": facility_name, "Full Lockdown": full_lockdown, "Partial Lockdown": partial_lockdown, "Date": current_date, "Time": now_cst, "Shift": shift})
            except Exception as e:
                results.append({"URL": facility_name, "Full Lockdown": False, "Partial Lockdown": False, "Error": str(e)})
        await browser.close()
    df = pd.DataFrame(results)
    print(df)
    return df # Return the DataFrame
asyncio.run(main())

lockdown_data = asyncio.run(main())
lockdown_data.to_csv(f'{current_date_str}_{current_hour_str}_{shift}_record.csv', index =False)

master_file = "master_lockdown.csv"

if os.path.exists(master_file):
    master_df = pd.read_csv(master_file)
    master_df = pd.concat([master_df,lockdown_data], ignore_index=True)
else:
    master_df = lockdown_data

master_df.to_csv(master_file, index=False)