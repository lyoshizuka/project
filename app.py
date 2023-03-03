import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from altair.expr import datum
import plotly.figure_factory as ff
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

st.title('K8s dashboard, interim solution ')

# define functions


def main():
    #data = load_data(nrows)
    page = st.sidebar.selectbox("Choose a page", ["Homepage", "Exploration"])

    if page == "Homepage":
        st.header("Welcome to the ad-hoc K8s Dashboard!")
        st.write("NOTE: Until the number of Tableau licenses can be augmented, this is an interim solution to data visualization for the Kubernetes squad.")
        st.write("DIRECTIONS: Please select a page on the left to start exploring data.")
        # st.write(df)
    elif page == "Exploration":
        st.title("Data Exploration")
        visualize_data(data)
       


@st.cache_data
def load_data():
    df = pd.read_csv(
        'Block_Storage_linked_to_kapsule_servers_2023_02_16 - [PAR1]_Block_Storage_linked_to_kapsule_servers_2023_02_16.csv')

    def lowercase(x): return str(x).lower()
    df.rename(lowercase, axis='columns', inplace=True)
    df['volume_creation_date'] = pd.to_datetime(df['volume_creation_date'])
    return df


data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Data loaded successfully! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)


def sort_offers(offer):
    return offer.split('-')
#offer_list= data(['offer_internal_name'])
#offer_list.sort(key=sort_offers)


def visualize_data(data):
    last_year = data[data.volume_creation_date > '2022-01-01 00:00:00']
   # sizes=['MICRO','NANO','XXS','XS','S','M','L','XL']

    st.subheader('Categorical Variable Distributions')
    storage = alt.Chart(data).mark_bar().encode(
        x=alt.X('volume_type:N', sort='descending'),
        y='count()'
    ).properties(
        title='Storage Type'
    ).interactive()
    storage
    offers = alt.Chart(data).mark_bar().encode(
        x=alt.X('offer_internal_name:N'),
        y='count()'
    ).properties(
        title='Offer Type'
    ).interactive()
    offers

    st.subheader('Most Popular Offer Configurations')
    correlation = alt.Chart(data).mark_bar().encode(
        x=alt.X('offer_internal_name:N', sort='y'),
        y='volumes_rank:Q',
        color=alt.Color('volume_type', type='nominal')
        #row='offer_internal_name:N'
    ).transform_aggregate(
        volumes_rank='sum(nb_volumes)',
        groupby=['offer_internal_name']
    ).transform_filter(
        (alt.datum.rank < 40 )
    ).properties(
        width=600, 
        height=600
    )
    st.write(correlation)

    st.subheader('Kapsule users linked to Block storage, MoM starting in 2022')
    last_year = data[data.volume_creation_date > '2022-01-01 00:00:00']
    graph1 = alt.Chart(last_year).encode(x='volume_creation_date:T').properties(
        width=1000, 
        height=800
    ).transform_filter(datum.volume_type == 'b_ssd')
    columns = sorted(data['offer_internal_name'].unique())
    selection = alt.selection_single(
        fields=['volume_creation_date'], nearest=True, on ='mouseover', empty='none', clear='mouseout'
    )
    
    bars = graph1.mark_bar().encode(y='nb_volumes:Q', color='offer_internal_name:N')
    points = bars.mark_point().transform_filter(selection)

    rule = graph1.transform_pivot(
        'offer_internal_name', value='nb_volumes', groupby=['volume_creation_date']
    ).mark_rule().encode(
        opacity=alt.condition(selection, alt.value(0.3), alt.value(0)),
        tooltip=[alt.Tooltip(c, type='quantitative') for c in columns]
    ).add_selection(selection)
    bars+points+rule

    st.subheader('Kapsule users linked to Local storage, MoM starting in 2022')
    graph2 = alt.Chart(last_year).encode(x='volume_creation_date:T').properties(
        width=1000, 
        height=800
    ).transform_filter(datum.volume_type == 'l_ssd')
    columns = sorted(data['offer_internal_name'].unique())
    selection = alt.selection_single(
        fields=['volume_creation_date'], nearest=True, on ='mouseover', empty='none', clear='mouseout'
    )
    
    bars = graph2.mark_bar().encode(y='nb_volumes:Q', color='offer_internal_name:N')
    points = bars.mark_point().transform_filter(selection)

    rule = graph2.transform_pivot(
        'offer_internal_name', value='nb_volumes', groupby=['volume_creation_date']
    ).mark_rule().encode(
        opacity=alt.condition(selection, alt.value(0.3), alt.value(0)),
        tooltip=[alt.Tooltip(c, type='quantitative') for c in columns]
    ).add_selection(selection)
    bars+points+rule

    st.subheader('Kapsule volumes by Instance offer & storage type')
    select=alt.selection_single(fields=['offer_internal_name'],on='mouseover', nearest=True,empty='none', clear='mouseout')
    graph = alt.Chart(data).mark_bar().encode(
        x='offer_internal_name',
        y='sum(nb_volumes)',
        color=alt.Color('volume_type', type='nominal'),
        tooltip=['volume_type', 'offer_internal_name'],
        order=alt.Order('offer_internal_name', sort='ascending')
    ).properties(
        width=800, 
        height=800
    ).interactive()

    text = alt.Chart(data).mark_text(color='black', baseline='middle', angle=270).encode(
        x=alt.X('offer_internal_name:N'),
        y=alt.Y('sum(nb_volumes):Q', stack='zero'),
        detail='volume_type:N',
        #text=alt.Text('sum(nb_volumes):Q', band=0.5)
    ).add_selection(select)
    graph + text

  



if __name__ == "__main__":
    main()
