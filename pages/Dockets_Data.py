# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 21:21:47 2023

@author: samda
"""

import pandas as pd
import streamlit as st
from config import docket_data_link, docket_codebook_link, dtype_dict_dock, filter_dataframe, load_data

# create sections on page
header = st.container()
data_section = st.container()

## header section
with header:
    st.title('Federal Circuit Docket Dataset')
    st.write("[The current codebook for the docket dataset may be downloaded here.](%s)" % docket_codebook_link)
    
## data section
with data_section:
    
    # read in data and display
    df_dock = load_data(docket_data_link, 
                        state_name = 'df_dock', dtype_dict = dtype_dict_dock)
    
    # set up columns for widgets
    col1, col2 = st.columns(2)
    
    # option to select columns to exclude from dataframe
    with col1:
        select_cols = st.checkbox("Select Variables")
        if select_cols:
            df_dock_cols = st.multiselect("Select Columns:", df_dock.columns)
            # include selected columns
            df_dock_cols = [col for col in df_dock.columns if col in df_dock_cols]
            # return dataframe with selected columns
            df_dock = df_dock[df_dock_cols]
    
    # convert data to streamlit DataFrame with filtering options
    with col2:
        df_dock_filtered = filter_dataframe(df_dock)
    st.dataframe(df_dock_filtered, use_container_width = True)
    
    # function to convert data to csv
    def convert_df(df):
        return df.to_csv(index = False).encode('utf-8')
    
    # convert filtered data to csv
    csv_dock = convert_df(df_dock_filtered)
    
    # download option
    st.download_button(label = 'Download Dataset', 
                       data = csv_dock,
                       file_name = 'federal_circuit_docket_dataset.csv',
                       mime = 'text/csv')
    st.write('Note: Download will reflect any filtering performed on the data')