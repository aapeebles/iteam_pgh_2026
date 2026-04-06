import pandas
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import geopandas as gpd
import pandas as pd
import numpy as np



# Load a local GeoJSON file
gdf = gpd.read_file("mapdata/Allegheny_County_Census_Tracts_2020_2458367900982142177.geojson")
gdf.dtypes

norm_data = pd.read_csv("normalized_data.csv")
norm_data.head()

norm_data['fips_str'] = norm_data["fips_str"].astype('str')

merged_gdf = gdf.merge(norm_data[["fips_str","risk_score"]], right_on="fips_str", left_on="GEOID")

merged_gdf.head()

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
merged_gdf.plot(column='risk_score', ax=ax, legend=True,
           cmap='OrRd',  # Colormap (e.g., 'Viridis', 'Blues', 'OrRd')
           legend_kwds={'label': "Risk Score",
                        'orientation': "horizontal"})

ax.set_axis_off()
fig.suptitle('Modified Social Vulnerability Score\n across Allegheny Census Tracks', fontsize=20) # The "Title"
fig.savefig('cloropleth.png', dpi=300)
fig.clear()


neihborhoods = gpd.read_file("mapdata/pittsburghpaneighborhoods.geojson")


combined = gpd.overlay(merged_gdf, neihborhoods, how='union',keep_geom_type=False)

allegheny = gpd.read_file("https://data.wprdc.org/dataset/73eb573e-cc12-4f29-8e69-17f7975c89cb/resource/501b2f84-ac1c-40a3-8099-e4e431f993df/download/alcogisallegheny-county-council-districts.geojson")
rivers = gpd.read_file("mapdata/Major_Rivers_1010120527129796882.geojson")


fig, ax = plt.subplots(1, 1, figsize=(15, 10))
merged_gdf.plot(column='risk_score', ax=ax, legend=True,
           cmap='OrRd',  # Colormap (e.g., 'Viridis', 'Blues', 'OrRd')
           legend_kwds={'label': "Risk Score",
                        'orientation': "vertical"})

ax.set_axis_off()
fig.suptitle('Modified Social Vulnerability Score by Census Tract\n within Allegheny Council Districts', fontsize=20) # The "Title"
rivers.plot(ax=ax, facecolor='blue', edgecolor='blue',linewidth=4)
allegheny.plot(ax=ax, facecolor='none', edgecolor='grey', linewidth=2)
allegheny.apply(lambda x: ax.annotate(text=x['LABEL'], xy=x.geometry.centroid.coords[0], ha='center'), axis=1)
fig.savefig('cloropleth2.png', dpi=300)
fig.clear()

allegheny.columns


### TOP 70%
merged_gdf['high_score'] = np.where(merged_gdf['risk_score']>=.7,1,0)
merged_gdf.high_score.value_counts()

fig, ax = plt.subplots(1, 1, figsize=(15, 10))

color_map = {True: 'red', False: 'white'}
merged_gdf['plot_color'] = (merged_gdf['risk_score'] > .7).map(color_map)
ax.set_axis_off()
fig.suptitle('Census Tracts with Risk Score Greater than 70%\n within Allegheny Council Districts', fontsize=20) # The "Title"

merged_gdf.plot(column = 'high_score', ax=ax, color=merged_gdf['plot_color'], edgecolor='grey', linewidth=.5)
allegheny.plot(ax=ax, facecolor='none', edgecolor='grey', linewidth=2)
allegheny.apply(lambda x: ax.annotate(text=x['LABEL'], xy=x.geometry.centroid.coords[0], ha='center'), axis=1)
rivers.plot(ax=ax, facecolor='blue', edgecolor='blue', linewidth=4)
fig.savefig('cloropleth4.png', dpi=300)
fig.clear()

top_70=merged_gdf['GEOID'].loc[merged_gdf['high_score']==1]
scores = merged_gdf[['GEOID', 'risk_score']]
scores.rename(columns={'GEOID':'fips_str'}, inplace=True)

### TOP 50%
merged_gdf['high_score'] = np.where(merged_gdf['risk_score']>=.5,1,0)
merged_gdf.high_score.value_counts()

fig, ax = plt.subplots(1, 1, figsize=(15, 10))

color_map = {True: 'red', False: 'white'}
merged_gdf['plot_color'] = (merged_gdf['risk_score'] > .5).map(color_map)

ax.set_axis_off()
fig.suptitle('Census Tracts with Risk Score Greater than 50% \n within Allegheny Council Districts', fontsize=20) # The "Title"

merged_gdf.plot(column = 'high_score', ax=ax, color=merged_gdf['plot_color'], edgecolor='grey', linewidth=.5)
allegheny.plot(ax=ax, facecolor='none', edgecolor='grey', linewidth=2)
rivers.plot(ax=ax, facecolor='blue', edgecolor='blue', linewidth=4)
allegheny.apply(lambda x: ax.annotate(text=x['LABEL'], xy=x.geometry.centroid.coords[0], ha='center'), axis=1)
fig.savefig('cloropleth5.png', dpi=300)
fig.clear()

#### TOP 50 with city boundary
pgh_outline = gpd.read_file("https://pghgishub-pittsburghpa.opendata.arcgis.com/datasets/a99f25fffb7b41c8a4adf9ea676a3a0b_0.geojson?outSR=%7B%22latestWkid%22%3A2272%2C%22wkid%22%3A102729%7D")
merged_gdf['high_score'] = np.where(merged_gdf['risk_score']>=.5,1,0)
merged_gdf.high_score.value_counts()

fig, ax = plt.subplots(1, 1, figsize=(15, 10))

color_map = {True: 'red', False: 'white'}
merged_gdf['plot_color'] = (merged_gdf['risk_score'] > .5).map(color_map)

ax.set_axis_off()
fig.suptitle('Census Tracts with Risk Score Greater than 50% \n within Allegheny Council Districts', fontsize=20) # The "Title"
rivers.plot(ax=ax, facecolor='blue', edgecolor='blue', linewidth=4)
pgh_outline.plot(ax=ax, facecolor='none', edgecolor='yellow', linewidth=3)
merged_gdf.plot(column = 'high_score', ax=ax, color=merged_gdf['plot_color'], edgecolor='grey', linewidth=.5)
allegheny.plot(ax=ax, facecolor='none', edgecolor='grey', linewidth=1)
# allegheny.apply(lambda x: ax.annotate(text=x['LABEL'], xy=x.geometry.centroid.coords[0], ha='center'), axis=1)
fig.savefig('cloropleth6.png', dpi=300)
fig.clear()


### ANALYSIS
percent_df=pd.read_csv('tract_percents.csv')
percent_df.head()
percent_df['fips_str'] = percent_df['fips_str'].astype('str')
percent_df.loc[percent_df.fips_str.isin(top_70.values.tolist())]
percent_df.dtypes
scores.dtypes

population_df = pd.read_csv("population_size.csv")
population_df['fips_str'] = population_df['fips_str'].astype('str')

analysis_df = percent_df.merge(scores, left_on='fips_str', right_on='fips_str',suffixes=("_x","_y"))
final_df = analysis_df.merge(population_df, left_on='fips_str', right_on='fips_str',suffixes=("_x","_y"))


ax = final_df[['pop']].boxplot()
ax.set_xticks([1])
ax.set_xticklabels(["Population Size"])
fig = ax.get_figure()
fig.suptitle('Range of Population Across Allegheny Census Tracts', fontsize=16, wrap=True) # The "Title"
fig.set_tight_layout(True)
fig.savefig('population_boxplot.png', dpi=300)
fig.clear()




final_df[['pop']].describe()
final_df[['ep_pov', "ep_bipoc", 'ep_carless', 'ep_overcrowd']].corr()

import seaborn as sns

# fig, ax = plt.subplots(1, 1, figsize=(15, 10))
corr_matrix = final_df[['ep_pov', "ep_bipoc", 'ep_carless', 'ep_overcrowd']].corr()

ax = sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
tick_labels = ["Percent Below\n150% Poverty", "Percent BIPOC", "Percent Household\n without a Car", "Percent of Housing\nOvercrowded"]
ax.set_xticks([.5,1.5,2.5,3.5])
ax.set_xticklabels(tick_labels, rotation=0, ha='right')
ax.set_yticks([.5,1.5,2.5,3.5])
ax.set_yticklabels(tick_labels,rotation=0, ha='right' )
fig = ax.get_figure()
fig.set_size_inches(10, 8) 
fig.suptitle('Heatmap of Correlation Matrix between Analysis Variables', fontsize=20)
# fig.set_tight_layout(True)
fig.savefig('corr_heatmap.png', dpi=300)
fig.clear()


final_df.sort_values(by='risk_score', ascending=False).head(10)
