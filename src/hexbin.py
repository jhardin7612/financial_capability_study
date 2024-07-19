import pandas as pd
import geopandas as gpd
from matplotlib.colors import Normalize
from utils import gen_big_3_df, gen_geo_df

df = csv_to_df("./data/2021-SxS-Data-and-Data-Info/partial_cleaned_2021.csv")




def gen_hexbin_map(df):
    #Create subset Df
    big_3 = gen_big_3_df(df)

    #Create geopandas df for graphs
    geoData = gen_geo_df(big_3)

    """
    Generated hexbin map based on user selection
    """
    # Initialize the figure
    fig, ax = plt.subplots(1, figsize=(13, 13))

    # Draw a map with matplotlib 
    geoData.plot(
        ax=ax, 
        column='fin_sat_avg',
        cmap="BuPu",
        edgecolor='black', 
        linewidth=.5,
        legend=False
    )
    # add a "centroid" column with the centroid position of each state
    geoData['centroid'] = geoData['geometry'].apply(lambda x: x.centroid)

    # for each state, annotate with the state name located at the centroid coordinates 
    for idx, row in geoData.iterrows():
        ax.annotate(
            text=row['iso3166_2'], 
            xy=row['centroid'].coords[0], 
            horizontalalignment='center', 
            va='center',
            color= 'black'
        )
    # Remove axis
    ax.axis('off')

    plt.title('Average Financial Satisfaction' , size= 20)

    # Add a color bar
    norm = Normalize(vmin=geoData['fin_sat_avg'].min(), vmax=geoData['fin_sat_avg'].max())
    sm = plt.cm.ScalarMappable(cmap='BuPu', norm=norm)
    sm.set_array([geoData['fin_sat_avg']]) 
    fig.colorbar(sm, orientation="horizontal",  aspect=50,fraction=0.005, pad=0, ax = ax )
    return fig