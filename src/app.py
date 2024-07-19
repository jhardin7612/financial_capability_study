"""
Generate Hexbin map of United states tht show various features related to financial capability study
"""
import streamlit as st
import pandas as pd
import sys
sys.path.insert(0,'.')
from hexbin import gen_hexbin_map

# Header 
st.markdown("# Exploring Financial Capability Across The United States of America")

#Description of Data
st.markdown("## [Data](https://finrafoundation.org/knowledge-we-gain-share/nfcs/data-and-downloads) Overview")
st.markdown("The National Financial Capability Study (NFCS)is a triannual survey designed to examine the financial capability as defined by the FINRA Foundation, of over 25,000 U.S. adults.")

#Sample From Original Data Frame Transposed, Scrollable?
st.caption("Sample From The Altered Dataset Transposed")

df = pd.read_csv("./data/2021-SxS-Data-and-Data-Info/partial_cleaned_2021.csv")
df = df.drop(columns='Unnamed: 0')
sample_df = df.sample(25)
st.dataframe(sample_df.T)

#Hexbin Maps
st.divider()
# # Get User Input
hb_option = st.selectbox("Select a different Feature to change the map",
            options= ['Finacial Satisfaction', 'Financial Confidence', 'Math Confidence'])

hb_map = gen_hexbin_map(df, hb_option)
st.pyplot(hb_map)