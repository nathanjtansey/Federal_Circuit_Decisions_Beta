import pandas as pd
import streamlit as st
import datetime
import plotly.express as px
import geopandas as gpd
from config import docket_data_link, document_data_link, dtype_dict_dock, dtype_dict, load_data

# create sections on page
header = st.container()
map_section = st.container()
line_section = st.container()
plot_section = st.container()


## header section
with header:
    st.title('Visualizations')

# read in data from dockets page (stored in session state)
if 'df_dock' in st.session_state:
    data = st.session_state['df_dock']
# if dockets page was not run yet, will need to read in data again
else:
    # read in data and display
    data = load_data(docket_data_link, 
                     state_name = 'df_dock', dtype_dict = dtype_dict_dock)

with map_section:
    st.subheader('Originating Tribunal Counts')
    
    # function that reads geoJSON data and caches it
    @st.cache_data()
    def read_geo(link):
        return gpd.read_file(link)

    # read data
    geo_data = read_geo("https://raw.githubusercontent.com/sdannels/Federal_Circuit_Decisions_Beta/main/Data/US_District_Court_Jurisdictions.geojson") # geojson data for plotting to district courts
    
    court_names = ['wdky', 'edky', 'sdind', 'mdala', 'sdala', 'wdark', 'edark', 'ndcal', 'edcal', 'cdcal', 'dcolo', 'ddc', 'mdfla', 'ndfla', 'mdga', 'sdga', 'ndga', 'didaho', 'dkan', 'ndtex', 'sdtex', 'wdtex', 'wdmo', 'edmo', 'dmont', 'dneb',
                'edwash', 'wdla', 'edla', 'dme', 'dmd', 'sdiowa', 'dnj', 'dnm', 'wdny', 'ndny', 'edny', 'wdnc', 'ednc', 'mdnc', 'dnd', 'ndohio', 'wdokla', 'edtex', 'dutah', 'edokla', 'dor', 'wdpa', 'edpa', 'mdpa', 'dsc', 'dsd', 'edtenn',
                'wdtenn', 'mdtenn', 'dmass', 'dhaw', 'sdill', 'wdva', 'wdwash', 'dvi', 'dminn', 'ndmiss', 'sdmiss', 'ndind', 'dnev', 'dnh', 'sdcal', 'dariz', 'ndwva', 'sdwva', 'wdwis', 'dwyo', 'dnmari', 'sdfla', 'ndokla', 'dvt', 'ddel',
                'edwis', 'sdohio', 'wdmich', 'sdny', 'dri', 'dalaska', 'ndill', 'dguam', 'dpr', 'edmich', 'ndiowa', 'cdill', 'dconn', 'ndala', 'mdla', 'edva'] # sets up correct order for mapping
    fid_list = range(0,94) # listing FID
    fid_df = pd.DataFrame(data = {"abbr": court_names, 'fids': fid_list})
    us_plot_df = data.groupby(['TribOfOrigin']).count().reset_index()
    us_plot_df['CourtOrigin'] = us_plot_df['TribOfOrigin'].str.replace('.', '').str.lower()
    us_merge = fid_df.merge(us_plot_df, how = 'left', on = None, left_on = 'abbr', right_on = 'CourtOrigin') # merges docket data with correct order fid_list
    us_merge = us_merge.fillna(0) # replaces NANs with 0 to represent no dockets from that court
    fig_us = px.choropleth(us_merge, geojson = geo_data, locations = 'fids', color = 'PACER_ID', # PACER_ID represents unique cases for each court
                        color_continuous_scale = 'plasma',
                        range_color = (0, 100), # Color scale for heat map component, adjustable to highlight any count differences
                        scope = 'usa',
                        labels = {'PACER_ID': 'Number of Cases'}) 
    fig_us.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_us)


with line_section:
    st.subheader('Federal Court Dispositions')
    
    # read in data from document data set (stored in session state)
    if 'df' in st.session_state:
        df1 = st.session_state['df']
    # if first page was not run yet, will need to read in data again
    else:
        df1 = load_data(document_data_link, 
                       state_name = 'df', dtype_dict = dtype_dict)
    
    df8 = df1.groupby(['docYear','DispGeneral']).count().reset_index()
    df8 = df8.rename(columns = {'uniqueID': 'Count'})
    fig8 = px.bar(df8, x = 'docYear', y = 'Count', color = 'DispGeneral', title = 'Dispositions')
    st.plotly_chart(fig8)


with plot_section:
    st.subheader('Filter Results by Year')
    
    start_date = st.date_input('Start Date', datetime.date(2004,10,1), min_value = datetime.date(2004,10,1), max_value = datetime.date.today() - datetime.timedelta(days=1) )
    end_date = st.date_input('End Date', datetime.date.today(), min_value = datetime.date(2004,10,2), max_value = datetime.date.today() )
    if start_date < end_date:
        st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
    else:
        st.error('Error: End date must fall after start date.')
    df1['docDate'] = pd.to_datetime(df1['docDate']).dt.date

    df_year_filter = df1[(df1['docDate'] > start_date) & (df1['docDate'] < end_date)]
    origin_df = df_year_filter.groupby('origin').count()
    fig_o = px.bar(origin_df.reset_index(), x = 'origin', y = 'uniqueID', title = 'Court Origins')
    st.plotly_chart(fig_o)
    
    
    yearXorigin_df = df_year_filter.groupby(['docYear','origin']).count()
    yearXorigin_df = yearXorigin_df.rename(columns = {'uniqueID': 'Count'})
    fig_yearo = px.bar(yearXorigin_df.reset_index(), x = 'docYear', y = 'Count', color = 'origin', title = 'Court Origins over Time')
    st.plotly_chart(fig_yearo)

    prec = df_year_filter.loc[df_year_filter['PrecedentialStatus'] == 'Precedential']
    prec_gp = prec.groupby(['DispGeneral']).count().reset_index()
    prec_gp = prec_gp.rename(columns = {'uniqueID': 'Count'})
    fig_prec = px.pie(prec_gp, values = 'Count', names = 'DispGeneral',title = 'Precedential Case Results')
    st.plotly_chart(fig_prec)

    no_prec = df_year_filter.loc[df_year_filter['PrecedentialStatus'] != 'Precedential']
    no_prec_gp = no_prec.groupby(['DispGeneral']).count().reset_index()
    no_prec_gp = no_prec_gp.rename(columns = {'uniqueID': 'Count'})
    no_fig_prec = px.pie(no_prec_gp, values = 'Count', names = 'DispGeneral',title = 'Non-Precedential Case Results')
    st.plotly_chart(no_fig_prec)