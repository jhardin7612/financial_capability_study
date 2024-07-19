import pandas as pd
import geopandas as gpd
##FUNCTIONS

def csv_to_df(file_path:str):
    """
    Loads CSV file into a dataframe

    Args:
        file_path (str) : file path to csv file
    Returns: pandas dataframe
    """
    return pd.read_csv(file_path)

def change_cat_vals(df, c_name, vals, labels):
    '''
        Replaces values of specifed column  in given dataframe
        **Does not modify original dataframe**

        Args:
            df (pandas dataframe): The data frame you want referenced
            c_name (str): name of column you want to manipulate
            vals (list): list of values you want replaced in column
            labels (list): list of values you want mapped to replace vals
        
        Returns:
            New dataframe with updated column value
    
    '''
    new_df = df.copy()
    replace_dict = dict(zip(vals, labels))
    new_df[c_name]=new_df[c_name].replace(replace_dict)
    return new_df

def gen_big_3_df(df):
    """
    Returns df with 3 key features for hexbin maps
    """
    feature_df = df[['state', 'math_conf_lvl', 'fin_sat_lvl', 'fin_conf_lvl']]

    # Define the columns and values to replace
    columns_dict = {
        'math_conf_lvl': [99, 98],
        'fin_sat_lvl': [99, 98],
        'fin_conf_lvl': [99, 98],

    }
    # Loop over the dictionary to replace the values
    for column, values in columns_dict.items():
        for value in values:
            feature_df.loc[feature_df[column] == value, column] = None
    feature_df = feature_df.dropna()
    return feature_df

def gen_geo_df(mini_df):
    """
    Creates the necessary df to make hexbins
    """
    state_math_avg =df[['state','math_conf_lvl']].groupby('state').mean().reset_index()
    state_math_avg=state_math_avg.sort_values(by='state')

    state_sat_avg =df[['state','fin_sat_lvl']].groupby('state').mean().reset_index()
    state_sat_avg=state_sat_avg.sort_values(by='state')

    fin_conf_avg = df[['state','fin_conf_lvl']].groupby('state').mean().reset_index()
    fin_conf_avg = fin_conf_avg.sort_values(by='state')
    # Load file
    url = "https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/us_states_hexgrid.geojson.json"
    geoData = gpd.read_file(url)
    # Add a new column to the geo dataframe that will be used for joining:
    geoData['state'] = geoData['google_name'].str.replace('(United States)','')
    # Sort by column: 'state' (ascending)
    geoData = geoData.sort_values(['state']).reset_index()
    # Drop column: 'bees'
    geoData = geoData.drop(columns=['bees', 'index'])
    #Create Columns from subsets
    geoData['fin_sat_avg'] = state_sat_avg['fin_sat_lvl']
    geoData['math_conf_avg'] = state_math_avg['math_conf_lvl']
    geoData['fin_conf_avg'] = fin_conf_avg['fin_conf_lvl']

    return geoData