import pandas as pd
from datetime import timedelta
from datetime import datetime, date
import pytz
import os

cst_timezone = pytz.timezone('US/Central')
now_cst = datetime.now(cst_timezone)
current_date = now_cst.date()
yesterday_date = current_date-timedelta(days=1)

df = pd.read_csv("./data/master_lockdown.csv")

df['Date'] = pd.to_datetime(df['Date'])

filtered_date = df[df['Date'].dt.date == current_date]

Daily_AGG = (
    filtered_date
        .groupby(['URL','Shift'])
        .agg(Date = ('Date','max'),
            Full_Lockdown = ('Full Lockdown', 'max'),
            Partial_Lockdown = ('Partial Lockdown', 'max'),
        )
        .reset_index()
)

master_file = './data/master_lockdown.csv'
daily_file = './data/daily_agg.csv'
os.makedirs('data', exist_ok=True)

if os.path.exists(daily_file):
    daily_df = pd.read_csv(daily_file)
    daily_df = pd.concat([daily_df, Daily_AGG], ignore_index=True)
else:
    daily_df = Daily_AGG
    
daily_df.to_csv(daily_file, index=False)

remaining_df = df[df['Date'].dt.date != yesterday_date]
remaining_df.to_csv(master_file, index=False)