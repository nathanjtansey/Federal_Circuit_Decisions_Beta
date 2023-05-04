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
    st.write("""Selecting the fields below will change the data used for the below visualization. The *Filter Data*
    selection will change the data being plotted, while selecting the variables changes which plot is displayed.""" )
    st.write(""" In addition to the dropdown menus, Plotly graphs are customizable or downloadable using the menu on 
    each individual graph.Clicking on a certain subfield in the Plotly menu will remove the subfield from the graph, allowing 
    for an alternative method of tuning visualizations. Double clicking on a subfield will only plot that specific subfield. """) 

with selection_section:
    
    # read in data and display
    df = load_data(document_data_link, 
                   state_name = 'df', dtype_dict = dtype_dict)
    
    # set up columns for widgets
    col1, col2 = st.columns(2)
    

    with col1: # filters the dataframe before selecting variables to select data based on non-graphing variables
        df_filtered = filter_dataframe(df)
    # option to select columns to exclude from dataframe
    with col2:
        select_cols = st.checkbox("Click Here to Select Variables")
        if select_cols:
            select_cols = st.multiselect("Select Columns:", # Limits selectable variables for graphing
                                     ['docYear', 'origin', 'PrecedentialStatus', 'DispGeneral'])
            df_cols = ['uniqueID'] + select_cols
            # include selected columns
            df_cols = [col for col in df_filtered.columns if col in df_cols]
            # return dataframe with selected columns
            df_filtered = df_filtered[df_cols]
    #st.dataframe(df_filtered.head(), use_container_width = True)
    
    
with graph_section:
    if select_cols: # checks whether any columns have been selected
        st.subheader('Graphs from Selected Data')
        # this if elif list can be changed in priority to show certain graphs over others
        # earlier statements have higher priority
        if 'origin' in df_cols and 'DispGeneral' in df_cols: # graphs only if certain columns were selected
            dfoD = df_filtered.groupby(['docYear','DispGeneral']).count().reset_index()
            dfoD = dfoD.rename(columns = {'uniqueID': 'Count'}) 
            figc = px.bar(dfoD, x = 'docYear', y = 'Count', color = 'DispGeneral', title = 'Dispositions',
                          color_discrete_sequence=px.colors.qualitative.Light24[2:])
            figc.update_layout(legend_traceorder="reversed")  # First plotted is at the bottom of legend      
        elif 'docYear' in df_cols and 'origin' in df_cols:
            yearXorigin_df = df_filtered.groupby(['docYear','origin']).count()
            yearXorigin_df = yearXorigin_df.rename(columns = {'uniqueID': 'Count'})
            figc = px.bar(yearXorigin_df.reset_index(), x = 'docYear', y = 'Count', 
                               color = 'origin', title = 'Court Origins over Time',
                               color_discrete_sequence=px.colors.qualitative.Light24[0:])
            figc.update_layout(legend_traceorder="reversed")
        elif 'DispGeneral' in df_cols:
            prec_gp = df_filtered.groupby(['DispGeneral']).count().reset_index()
            prec_gp = prec_gp.rename(columns = {'uniqueID': 'Count'})
            figc = px.pie(prec_gp, values = 'Count', names = 'DispGeneral',title = 'Case Results',
                          color_discrete_sequence=px.colors.qualitative.Light24[2:])
        elif 'origin' in df_cols:
            origin_df = df_filtered.groupby('origin').count()
            origin_df = origin_df.rename(columns = {'uniqueID': 'Count'})
            figc = px.bar(origin_df.reset_index(), x = 'origin', y = 'Count', title = 'Court Origins',
                          color_discrete_sequence=px.colors.qualitative.Light24[2:])
            figc.update_layout(legend_traceorder="reversed")
        elif 'docYear' in df_cols:
            year_df = df_filtered.groupby(['docYear']).count().reset_index()
            year_df = year_df.rename(columns = {'uniqueID': 'Count'})
            figc = px.bar(year_df, x = 'docYear', y = 'Count', title = 'Number of Court Cases',
                          color_discrete_sequence=px.colors.qualitative.Light24[2:])
            figc.update_layout(legend_traceorder="reversed")
            

        try: # checks if a plot has been generated 
            #figc
            st.plotly_chart(figc) # plots list selected by columns
        except: # if no plot has been created, prompts the user to select more or different variables
            st.write("No graphs available for the selected variable(s)")