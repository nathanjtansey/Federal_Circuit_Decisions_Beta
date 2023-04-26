# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 21:40:38 2023

@author: samda
"""

import pandas as pd
import streamlit as st
from config import load_data, docket_data_link, dtype_dict_dock

# read in data from dockets page (stored in session state)
if 'df_dock' in st.session_state:
    df_dock = st.session_state['df_dock']
# if dockets page was not run yet, will need to read in data again
else:
    # read in data and display
    df_dock = load_data(docket_data_link, 
                        state_name = 'df_dock', dtype_dict = dtype_dict_dock)
    
# set up section for searching for case
docket_search_section = st.container()

## case search section
with docket_search_section:
    # title section
    st.header('Search for a Specific Docket')
    
    # function to output search results
    def search_results(search_out):
        # throw error if zero or more than one case match criteria
        if len(search_out) > 1:
            st.error('There is more than one case matching your search criteria.' \
                     ' Please be more specific in your search. You may try using' \
                     ' the "Filter Data" button on the "Dockets Data" page to search the data.', 
                     icon="🚨")
        elif len(search_out) == 0:
            st.error('No cases match this search criteria.', 
                     icon="🚨")
        else:
            # transpose dataframe and print
            return st.dataframe(search_out.T, height=(1000), width=(1000))
        
    # search by Pacer ID
    # accept user input for pacer ID
    dock_search = st.text_input('Search by Pacer ID')
    # ignore empty search results
    if dock_search == '':
        pass
    # if user input text, try to match and output case
    else:
        # match uniqueID column to given case number
        search_out = df_dock[df_dock['PACER_ID'].astype(str) == dock_search]
        search_results(search_out)
