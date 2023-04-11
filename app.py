import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import plotly.express as px

# Initialize a session state variable that tracks the sidebar state (either 'expanded' or 'collapsed').
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'

# Set page configs
st.set_page_config(page_title='Data Visualization App', page_icon=':chart_with_upwards_trend:', layout='wide', initial_sidebar_state=st.session_state.sidebar_state)

# Toggle sidebar state between 'expanded' and 'collapsed'.
if st.button('Options'):
    st.session_state.sidebar_state = 'collapsed' if st.session_state.sidebar_state == 'expanded' else 'expanded'
    # Force an app rerun after switching the sidebar state.
    st.experimental_rerun()

# Set sidebar title
st.sidebar.title('Data Types')

# Define function to generate data
def generate_data(data_type, data_size):
    if data_type == 'Normal':
        data = np.random.normal(size=data_size) * 100
        summary = 'A normal distribution is a type of continuous probability distribution for a real-valued random variable.'
    elif data_type == 'Non-Normal':
        data = np.random.uniform(size=data_size) * 100
        summary = 'Non-normal distributions are any distribution that is not normal, such as uniform or exponential distributions.'
    elif data_type == 'Random':
        data = np.random.random(size=data_size) * 100
        summary = 'A random distribution generates random numbers with no underlying pattern or relationship.'
    elif data_type == 'Linear':
        data = np.linspace(0, 1, data_size) * 100
        summary = 'A linear distribution generates data points that are evenly spaced between two endpoints.'
    elif data_type == 'Exponential':
        data = np.random.exponential(size=data_size) * 100
        summary = 'An exponential distribution is a continuous probability distribution that models the time between events in a Poisson process.'
    elif data_type == 'Poisson':
        data = np.random.poisson(size=data_size) * 100
        summary = 'A Poisson distribution is a discrete probability distribution that models the number of events occurring in a fixed time interval.'
    elif data_type == 'Gamma':
        data = np.random.gamma(size=data_size, shape=2) * 100
        summary = 'A gamma distribution is a continuous probability distribution that models the time until a specified number of events occur in a Poisson process.'
    elif data_type == 'Skewed':
            data = np.random.random(size=data_size) * 100
            data = (data - np.mean(data)) / np.std(data)  # standardize data
            skewness = 10  # specify skewness parameter
            data = abs((data ** 2 + skewness) * np.sign(data))
            summary = 'A skewed distribution is a type of non-symmetric probability distribution that has a longer tail on one side than the other.'
    else:
        data = []
        summary = ''
    return data, summary

# Define function to plot data
def plot_data(data, plot_type):
    if plot_type == 'Line Chart':
        fig = px.line(x=np.arange(len(data)), y=data)
    elif plot_type == 'Histogram':
        fig = px.histogram(x=data, nbins=20)
    elif plot_type == 'Scatterplot':
        fig = px.scatter(x=np.arange(len(data)), y=data)
    elif plot_type == 'Heatmap':
        z, x, y = np.histogram2d(np.arange(len(data)), data, bins=[20, 20])
        fig = px.imshow(z, x=x[:-1], y=y[:-1])
    elif plot_type == 'Box and Whisker Plot':
        fig = px.box(x=data)
    elif plot_type == 'Bar Chart':
        df = pd.DataFrame({'x': np.arange(len(data)), 'y': data})
        fig = px.bar(df, x='x', y='y')
    else:
        fig = None
    return fig

# Define sidebar inputs
data_type = st.sidebar.selectbox('Select Data Type', ('Normal', 'Non-Normal', 'Random', 'Linear', 'Exponential', 'Poisson', 'Gamma', 'Skewed'))
data_size = st.sidebar.slider('Select Data Size', min_value=10, max_value=1000, step=10, value=350)
plot_type = st.sidebar.selectbox('Select Plot Type', ('Histogram', 'Line Chart', 'Scatterplot', 'Heatmap', 'Box and Whisker Plot', 'Bar Chart'))

# Generate data and summary
data, summary = generate_data(data_type, data_size)

# Set page title
st.title(f"Visualization of {data_type} Distribution")

# Display summary
st.write(summary)

# Plot data
if len(data) > 0:
    st.write(plot_type)
    fig = plot_data(data, plot_type)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning('Please select a data type')

# Add refresh button
if st.button('Refresh Data'):
    data, summary = generate_data(data_type, data_size)

# Set the link and the display text
link = 'https://github.com/DovarFalcone/beautifulcharts'
text = 'beautifulcharts'

# Show footer with the link
components.html(f'<div style="color:white">Created using the help of ChatGPT with ❤️. View <a href="{link}" target="_blank" style="color:white">{text}</a> on GitHub.</div>', height=30)
