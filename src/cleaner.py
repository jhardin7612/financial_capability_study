import pandas as pd

##FUNCTIONS

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

##PIPELINE