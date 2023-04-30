# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 13:50:04 2023

@author: samda
"""
import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
########### Set up documents data set ##############
# link to document data (*should not change*)
document_data_link = 'https://raw.githubusercontent.com/sdannels/Federal_Circuit_Decisions_Beta/main/Data/documents.tab'

# link to document codebook
document_codebook_link = 'https://dataverse.harvard.edu/api/access/datafile/6907843'

# define datatypes for document variables that need coverting
# if adding variables and filtering doesn't automatically work,
# add correct data type to dictionary below and clear cache on website
dtype_dict = {'uniqueID': str, 'docYear': int, 'origin': 'category',
              'docType': 'category', 'DisputeType': 'category', 
              'Dispute_General': 'category', 'utilityPatent': 'category', 
              'designPatent': 'category', 'plantPatent': 'category',
              'designPatent_old': 'category', 'Appellant_Type_Primary': 'category',
              'Dissent': 'category', 'Concurrence': 'category'}

########## Set up dockets data set ################
# link to docket data (*should not change*)
docket_data_link = 'https://raw.githubusercontent.com/sdannels/Federal_Circuit_Decisions_Beta/main/Data/dockets.tab'

# link to dockets codebook
docket_codebook_link = 'https://empirical.law.uiowa.edu/sites/empirical.law.uiowa.edu/files/wysiwyg_uploads/codebook_for_the_docket_dataset_-_2021-08-24.pdf'

# define datatypes for docket variables that need coverting
# if adding variables and filtering doesn't automatically work,
# add correct data type to dictionary below and clear cache on website
dtype_dict_dock = {'Year_Appeal_Filed': int, 'PACER_Gen': 'category',
                   'DistrictCourt': 'category', 'District_Court': 'category', 
                   'FY_Appeal_Filed': 'Int64'}

########### Functions ###################
# define function to load data
# st.cache_data means the data is stored and doesn't need to be read again each time the user changes a variable
@st.cache_data
def load_data(data_path, state_name, dtype_dict):
    '''
    Parameters
    ----------
    data_path : str
        The file path to load the data
    state_name : str
        The name that the DataFrame will be stored as in the session state

    Returns
    -------
    df : DataFrame
    '''
    df = pd.read_csv(data_path, sep = '\t', dtype = dtype_dict)
    # save the data in the session_state so it can be accessed from other pages
    st.session_state[state_name] = df
    return df


# define function to filter data
# see blog: https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/
def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Click Here to Filter Data")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        # local time zone conversion
        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            
            # Select categories for categorical data type
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
                
            # slider for numeric data type
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                # step size of 1 for integers
                if df[column].dtype in ['int64', 'Int64']:
                    step = float(1)
                # smaller step size for floats
                else:
                    step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
                
            # date range for datetime64 data type
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
                    
            # treat everything else like a string
            # search function for strings
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input, case = False)]

    return df