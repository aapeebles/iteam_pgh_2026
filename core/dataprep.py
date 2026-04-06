"""
Reads in filtering and rename variables from env and metadata
"""

import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick






load_dotenv()  # Loads variables from .env into os.environ

data_url = os.getenv('DATA_SOURCE')
sheet_id = os.getenv('SPREADSHEET_SHEET_ID')
sheet_name = os.getenv('SHEET_NAME')
county = os.getenv('COUNTY')
state = os.getenv('STATE')

print(sheet_id)

# data[0]['DATA_SOURCE']

with open('metadata/columns.txt', "r",encoding="utf-8") as col_names:
    col_data = col_names.readlines()

rename_dict = {line.split(":")[0]:line.split(":")[1].rstrip("\n") for line in col_data}


url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url)

raw_data = df[rename_dict.keys()]
raw_data_usable = raw_data.rename(columns=rename_dict)
raw_data_usable.dtypes

raw_data_usable.shape
raw_data_usable.describe()

# filter on allegheny county
raw_data_allegheny = raw_data_usable.loc[(raw_data_usable.county==county) & (raw_data_usable.state==state)]
raw_data_allegheny.shape
raw_data_allegheny.describe()

# start to
silver_one = raw_data_allegheny
silver_two = silver_one.assign(fips_str = silver_one.fips.astype('str'))

# convert to percentages
silver_two.columns
silver_two.dtypes



silver_three = silver_two.assign(ep_pov = ((silver_two["poverty"] / silver_two["pop"])).astype('float') )
silver_three["ep_bipoc"] = ((silver_three["bipoc"] / silver_three["pop"]) ).astype('float') 
silver_three["ep_carless"] = ((silver_three["carless"] / silver_three["households"])).astype('float') 
silver_three['ep_overcrowd'] = (silver_three["overcrowds"]/100).astype('float')



silver_four = silver_three[["fips_str", "ep_pov", "ep_bipoc", "ep_carless", "ep_overcrowd"]]
silver_four[["ep_pov", "ep_bipoc", "ep_carless", "ep_overcrowd"]].describe().sort_values(by=["ep_pov"])


ax = silver_four[["ep_pov", "ep_bipoc", "ep_carless", "ep_overcrowd"]].boxplot()
# Save the current figure to a file

ax.set_xticks([1, 2, 3, 4])
ax.set_xticklabels(['Poverty', 'BIPOC', 'Carless', "Overcrowded"])
ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

# Get the figure associated with that axes and save it
fig = ax.get_figure()
fig.suptitle('Range of Social Vulnerability Indicators\n across Allegheny Census Tracks', fontsize=16) # The "Title"
fig.text(0.5, 0.02, 'Calculated by percent of total population or total households respectively', 
         ha='center', fontsize=10, wrap=True)
fig.savefig('boxplot_details.png', dpi=300)


# normalized columns
numeric_cols = silver_four.select_dtypes(include=float)
normalized_df=(numeric_cols-numeric_cols.min())/(numeric_cols.max()-numeric_cols.min())
normalized_columns = {x:x.replace("ep_", "epn_") for x in normalized_df.columns.to_list()}
normalized_df.rename(columns=normalized_columns,inplace=True)
normalized_df = normalized_df.join(silver_four[["fips_str"]])

cols = list(normalized_columns.values())
cols
normalized_df[cols] = normalized_df[cols].mask(normalized_df[cols] < .1, 0)
normalized_df[cols] = normalized_df[cols].mask(normalized_df[cols] > .9, 1)



normalized_df['Row_Total'] = normalized_df.sum(axis=1, numeric_only=True)
normalized_df['risk_score']=(normalized_df['Row_Total']-normalized_df['Row_Total'].min())/(normalized_df['Row_Total'].max()-normalized_df['Row_Total'].min())
normalized_df.loc[normalized_df['risk_score']>0.9]
normalized_df.to_csv("normalized_data.csv", index=False)
silver_four.to_csv("tract_percents.csv")
silver_two[['pop','fips_str']].to_csv("population_size.csv")

