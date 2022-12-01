import streamlit as st
import numpy as np
import pandas as pd
import streamlit as st
import os


import yfinance as yf
from plotly import graph_objs as go


import datetime
from datetime import date

import requests



# - - - Title - - -
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# - - - Header Section - - -
with st.container():
    #st.subheader("Stock Market Data Analysis")
    st.title("Baltic Dry Index Prediction Model")



# ------ layout setting---------------------------
window_selection_c = st.sidebar.container() # create an empty container in the sidebar
window_selection_c.markdown("## Insights") # add a title to the sidebar container
# sub_columns = window_selection_c.columns(2) #Split the container into two columns for start and end date

# ------ REQUESTING THE API ON GCLOUD RUN ---------------------------

#currently the url only runs the local uvicorn instance.
url = "https://bdi-predict-wm54mkyava-an.a.run.app/predict"
response = requests.get(url).json()
print(response)
prediction = response["prediction"]
print(prediction)
prev_value = response["prev_value"]
print(prev_value)
delta=round((prediction-prev_value),2)
rate=round((delta/prev_value),2)

# - - - Button Returning a Value - - -

if st.button('Predict Model'):
    st.metric(label="BALTIC DRY INDEX", value=f'{round(prediction,2)} Points', delta=f'{delta} ({rate}%)')
else:
    st.write(' ')

#difference = prediction - prev_day
#change = difference/prev_day

# def show_delta(self):
#         """
#         Returning a predicted value for the BDI Index
#         """

#         cols = st.columns(2)
#         (color, marker) = ("green", "+") if difference >= 0 else ("red", "-")

#         cols[0].markdown(
#             f"""<p style="font-size: 90%;margin-left:5px">{self.symbol} \t {e}</p>""",
#             unsafe_allow_html=True
#         )
#         cols[1].markdown(
#             f"""<p style="color:{color};font-size:90%;margin-right:5px">{marker} \t {difference} {marker} {change} % </p>""",
#             unsafe_allow_html=True
#         )




# # - - - Date Selection - - -
# def nearest_business_day(DATE: datetime.date):
#     """
#     Takes a date and transform it to the nearest business day
#     """
#     if DATE.weekday() == 5:
#         DATE = DATE - datetime.timedelta(days=1)

#     if DATE.weekday() == 6:
#         DATE = DATE + datetime.timedelta(days=1)
#     return DATE

# ----------Time window selection-----------------
# YESTERDAY=datetime.date.today()-datetime.timedelta(days=1)
# YESTERDAY = nearest_business_day(YESTERDAY) #Round to business day

# DEFAULT_START=YESTERDAY - datetime.timedelta(days=10193)
# DEFAULT_START = nearest_business_day(DEFAULT_START)

# START = sub_columns[0].date_input("From", value=DEFAULT_START, max_value=YESTERDAY - datetime.timedelta(days=1))
# END = sub_columns[1].date_input("To", value=YESTERDAY, max_value=YESTERDAY, min_value=START)

# START = nearest_business_day(START)
# END = nearest_business_day(END)


# - - - Creating the Chart - - -
# ---------------stock selection------------------
STOCK = np.array([ "BDI", "CIP - YoY", "Nickel - Global Price"])
SYMB = window_selection_c.selectbox("Select Index", STOCK)


#Features:



if SYMB=='BDI':
    data=pd.read_csv("./streamlit_data/cleaned_weekly_BDI.csv")
elif SYMB=='CIP - YoY':
    data=pd.read_csv("./streamlit_data/weekly_cleanred_cip.csv")
elif SYMB=="Nickel - Global Price":
    data=pd.read_csv("./streamlit_data/cleaned_important_features_data.csv")





# In [22]: start = df.index.searchsorted(dt.datetime(2013, 1, 2))

# In [23]: end = df.index.searchsorted(dt.datetime(2013, 1, 4))

# df.iloc[START:END]

# Plot raw data
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['time'], y=data['close'], name="stock", text=data['time']))
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)
    st.plotly_chart(fig)

plot_raw_data()


@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, END)
    data.reset_index(inplace=True)
    return data




















# data_load_state = st.text('Loading...')
# data_load_state.text('Data displayed below!')

# - - - Creating the Slider - - -




# def get_slider_data():
#     el_nino=pd.read_csv("raw_data/data/Climate Data/el_nino.csv")
#     return pd.DataFrame({
#           'first column': el_nino['time'],
#           'Predicted Number': el_nino['Temperature']
#         })

# df = get_slider_data()

# from datetime import datetime
# start_time = st.slider(
#     "When do you want to start?",
#     value=datetime(1995, 1, 1),
#     format="MM/DD/YY")
# st.write("Start time:", start_time)

# filtered_df = df[df['first column'] % start_time]

# st.write(df)


# # - - - Feature Drop Down - - -
# def get_select_box_data():

#     return pd.DataFrame({
#           'first column': list(range(1, 11)),
#           'second column': np.arange(10, 101, 10)
#         })

# df = get_select_box_data()

# option = st.selectbox('Select a line to filter', df['first column'])

# filtered_df = df[df['first column'] == option]

# st.write(filtered_df)


# - - - Value Output Box - - -



# - - - Error Graph - - -
