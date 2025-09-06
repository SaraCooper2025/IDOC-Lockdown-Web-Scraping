## IDOC Lockdown Web Scraping
The Illinois Department of Corrections (IDOC) maintains an ongoing record of the number of lockdowns at each of its facilities, which are reported in several publicly available documents including their yearly [Operatations and Maintenance Reports](https://idoc.illinois.gov/reportsandstatistics/operation-and-management-reports.html) and, as of July 2025, quarterly [Restrictive Housing Reports](https://idoc.illinois.gov/reportsandstatistics/restrictivehousingreports.html).

Lockdown status is also provided on an up-to-date basis online, both on the IDOC [lockdown information](https://idoc.illinois.gov/facilities/lockdowninformation.html) webpage and on each individual facility's webpage. As this information needs to be updated for visitors in real time, it may provide a more accurate glimpse into the lockdown status of each prison within the IDOC than end-of-the-month compilations.

This project aims to assess the accuracy and consistency of official reporting across IDOC facilities by scraping their webpages for lockdown status on an hourly basis, compiling a daily log of the incidence of full and partial lockdowns for each of three shifts.

This code can be amended to scrape dynamic html for (a) defined keyword(s) from any provided list of URLs and then to produce logs which are updated on an hourly or daily basis.

## Install
This installation runs on Python 3.11.9

Install the [required packages](./requirements.txt) by running:

```sh
pip install -r requirements.txt
```
## Using This Code
This code is set up to run automatically without user intervention. It observes a list of URLs that direct to the facility pages for each of 26 IDOC facilities. Using the [PlayWright](https://playwright.dev/python/docs/intro) library, each site is scraped for defined keywords ("no visits" for full lockdown status and "limited visits" for paritial lockdown status). This outputs a csv file that includes the:
- facility name
- full lockdown status (0,1)
- partial lockdown status (0,1)
- date
- time
- shift (1,2,3)

Using the [main.yml](.github/workflows/main.yml) file, this command is run each hour on the hour. This is to account for the possibility of a facility being listed and unlisted on full or partial lockdown in the same shift. Updated daily, [daily_scrape.csv](.data/daily_scrape.csv) aggregates each hour's data.

Each day at 1 a.m. CST, [daily_aggregate.yml](.github/workflows/daily_aggregate.yml) consolidates daily data into the [master_tracker.csv](.data/master_tracker.csv). At the same time, this action deletes all previous day's data from [daily_scrape.csv](.data/daily_scrape.csv) to start fresh each day.

## Maintainers
[@SaraCooper2025](https://github.com/SaraCooper2025)


## License

© 2025 Sara Cooper
