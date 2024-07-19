import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from utils import gen_big_3_df, gen_geo_df

df = pd.read_csv("./data/2021-SxS-Data-and-Data-Info/partial_cleaned_2021.csv")


def gen_hexbin_map(df, feature):
    """
    Generated hexbin map based on user selection
    """

    options = {
        'Finacial Satisfaction': 'fin_sat_avg', 
        'Financial Confidence': 'fin_conf_avg', 
        'Math Confidence': 'math_conf_avg'
    }

    selection = [options[feature]]

    #Create subset Df
    big_3 = gen_big_3_df(df)

    #Create geopandas df for graphs
    gpd_df = gen_geo_df(big_3)

   
    # Initialize the figure
    fig, ax = plt.subplots(1, figsize=(13, 13))

    # Draw a map with matplotlib 
    gpd_df.plot(
        ax=ax, 
        column=selection[0],
        cmap="BuPu",
        edgecolor='black', 
        linewidth=.5,
        legend=False
    )
    # add a "centroid" column with the centroid position of each state
    gpd_df['centroid'] = gpd_df['geometry'].apply(lambda x: x.centroid)

    # for each state, annotate with the state name located at the centroid coordinates 
    for idx, row in gpd_df.iterrows():
        ax.annotate(
            text=row['iso3166_2'], 
            xy=row['centroid'].coords[0], 
            horizontalalignment='center', 
            va='center',
            color= 'black'
        )
    # Remove axis
    ax.axis('off')

    plt.title(f'Average {feature}' , size= 20)

    # Add a color bar
    norm = Normalize(vmin=gpd_df[selection[0]].min(), vmax=gpd_df[selection[0]].max())
    sm = plt.cm.ScalarMappable(cmap='BuPu', norm=norm)
    sm.set_array([gpd_df[selection[0]]]) 
    fig.colorbar(sm, orientation="horizontal",  aspect=50,fraction=0.005, pad=0, ax = ax )
    return fig