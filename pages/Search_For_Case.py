# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 20:11:08 2023

@author: samda
"""

import pandas as pd
import streamlit as st
from config import load_data, document_data_link, dtype_dict

# read in data from first page (stored in session state)
if 'df' in st.session_state:
    df = st.session_state['df']
# if first page was not run yet, will need to read in data again
else:
    df = load_data(document_data_link, 
                   state_name = 'df', dtype_dict = dtype_dict)

# set up section for searching for case
case_search_section = st.container()

## case search section
with case_search_section:
    # title section
    st.header('Search for a Specific Case')
    
    # give option to search by case ID or case name
    search_option = st.selectbox('Search By:', ['Unique ID', 'Case Name'])
    
    # function to output search results
    def search_results(search_out):
        # throw error if zero or more than one case match criteria
        if len(search_out) > 1:
            st.error('There is more than one case matching your search criteria.' \
                     ' Please be more specific in your search. You may try using' \
                     ' the "Filter Data" button on the home page to search the data.', 
                     icon="🚨")
        elif len(search_out) == 0:
            st.error('No cases match this search criteria.', 
                     icon="🚨")
        else:
            # transpose dataframe and print
            return st.dataframe(search_out.T, height=(1000), width=(1000))
        
    
    # search function depends on choice in search_option
    # search by UniqueID
    if search_option == 'Unique ID':
        # accept user input for case number
        case_search = st.text_input('Search by uniqueID')
        # ignore empty search results
        if case_search == '':
            pass
        # if user input text, try to match and output case
        else:
            # match uniqueID column to given case number
            search_out = df[df['uniqueID'].astype(str) == case_search]
            search_results(search_out)
    
    # or search by caseName
    else:
        # accept text input from user
        case_search = st.text_input('Case Name')
        # ignore empty search results
        if case_search == '':
            pass
        # if user input text, try to match and output case
        else:
            # match partial string to caseName in df
            search_out = df[df['caseName'].astype(str).str.contains(case_search, case = False)]
            # output results
            search_results(search_out)