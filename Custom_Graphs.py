import pandas as pd
import streamlit as st
import datetime
import plotly.express as px
import geopandas as gpd
from config import docket_data_link, document_data_link, dtype_dict_dock, dtype_dict, load_data, filter_dataframe

header = st.container()
selection_section = st.container()
graph_section = st.container()

with header:
    st.title('Customizable Visualizations') # Name of the subpage
    st.write("""Selecting the fields below will filter the data to use for the below visualizations. In addition to the
     dropdown menus, Plotly graphs are customizable or downloadable using the menu on each individual graph.""")
    st.write("""Clicking on a certain subfield in the Plotly menu will remove the subfield from the graph, allowing for an
    alternative method of tuning visualizations. """) 

with selection_section:
    
    # read in data and display
    df = load_data(document_data_link, 
                   state_name = 'df', dtype_dict = dtype_dict)
    
    # set up columns for widgets
    col1, col2 = st.columns(2)
    
    # option to select columns to exclude from dataframe
    with col1:
        select_cols = st.checkbox("Click Here to Select Variables")
        if select_cols:
            select_cols = st.multiselect("Select Columns:", # Limits selectable variables for graphing
                                     ['docYear', 'origin', 'PrecedentialStatus', 'DispGeneral'])
            df_cols = ['uniqueID'] + select_cols
            # include selected columns
            df_cols = [col for col in df.columns if col in df_cols]
            # return dataframe with selected columns
            df = df[df_cols]
    
    # convert data to streamlit DataFrame with filtering options
    with col2:
        df_filtered = filter_dataframe(df)
    st.dataframe(df_filtered.head(), use_container_width = True)

    
with graph_section:
    if select_cols: # checks whether any columns have been selected
        st.subheader('Graphs from Selected Data')
        # this if elif list can be changed in priority to show certain graphs over others
        # earlier statements have higher priority
        if 'origin' in df_cols and 'DispGeneral' in df_cols: # graphs only if certain columns were selected
            df8 = df_filtered.groupby(['docYear','DispGeneral']).count().reset_index()
            df8 = df8.rename(columns = {'uniqueID': 'Count'})
            figc = px.bar(df8, x = 'docYear', y = 'Count', color = 'DispGeneral', title = 'Dispositions')
            #st.plotly_chart(fig8)
        elif 'docYear' in df_cols and 'origin' in df_cols:
            yearXorigin_df = df_filtered.groupby(['docYear','origin']).count()
            yearXorigin_df = yearXorigin_df.rename(columns = {'uniqueID': 'Count'})
            figc = px.bar(yearXorigin_df.reset_index(), x = 'docYear', y = 'Count', 
                               color = 'origin', title = 'Court Origins over Time')        
        elif 'PrecedentialStatus' in df_cols and 'DispGeneral' in df_cols:
            # prec = df_filtered.loc[df_filtered['PrecedentialStatus'] == 'Precedential']
            prec_gp = df_filtered.groupby(['DispGeneral']).count().reset_index()
            prec_gp = prec_gp.rename(columns = {'uniqueID': 'Count'})
            figc = px.pie(prec_gp, values = 'Count', names = 'DispGeneral',title = 'Case Results')
        elif 'origin' in df_cols:
            origin_df = df_filtered.groupby('origin').count()
            figc = px.bar(origin_df.reset_index(), x = 'origin', y = 'uniqueID', title = 'Court Origins')
            #st.plotly_chart(fig_o)

        try: # checks if a plot has been generated 
            #figc
            st.plotly_chart(figc) # plots list selected by columns
        except: # if no plot has been created, prompts the user to select more or different variables
            st.write("No graphs available for the selected variable(s)")