import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

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
        x_axis = st.selectbox("Choose a variable for the x-axis", data.columns, index=3)
        y_axis = st.selectbox("Choose a variable for the y-axis", data.columns, index=4)
        visualize_data(data, x_axis, y_axis)


@st.cache_data
def load_data(nrows):
    df = pd.read_csv(
        'Block_Storage_linked_to_kapsule_servers_2023_02_16 - [PAR1]_Block_Storage_linked_to_kapsule_servers_2023_02_16.csv', nrows=nrows)

    def lowercase(x): return str(x).lower()
    df.rename(lowercase, axis='columns', inplace=True)
    df['volume_creation_date'] = pd.to_datetime(df['volume_creation_date'])
    return df


data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Data loaded successfully! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)


def visualize_data(data, x_axis, y_axis):
    st.subheader('Number of Kapsule users linked to Block storage')
    graph = alt.Chart(data).mark_bar().encode(
        x=x_axis,
        y=y_axis,
        color='offer_internal_name',
        tooltip=['volume_type', 'offer_internal_name', 'volume_type1', 'storage_size']
    ).interactive().properties(width=800, height=800)

    st.write(graph)


if __name__ == "__main__":
    main()
