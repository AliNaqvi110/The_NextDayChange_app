import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from Arima import  arima
from LSTM import forecast_high_low_lstm


# Load your S&P 500 data from a CSV file (Adjust the path to your file)
@st.cache_data
def load_data():
    data = pd.read_csv("data/USA500IDXUSD_D1.csv", sep="\t")
    # print(data.head())   # Just to have a look at data
    return data

def main():
    # set layout
    st.set_page_config(page_title="\U0001F4C8 Future Stock Price Prediction", page_icon=":chart_increasing:")

    # load the data from a file
    data = load_data()
    
    data['Time'] = pd.to_datetime(data['Time']) # to convert Time column to datetime type
    

    # Checkboxes to filter data based on high-impact news
    st.sidebar.subheader("Filter Data")
    high_impact_news = st.sidebar.checkbox("Include Only High Impact News Days", value=False)

    # set header and logo 
    # Display the logo image
    logo_image = "assets/git-turbo1.png"
    # st.image(logo_image, width=100, height=100)

    # Add a custom header with logo
    header_html = """
        <div style="display: flex; align-items: center;">
            <img src="{}" style="width: 50px; height: 50px; margin-right: 10px;">
            <h1>Future Stock Price Prediction 📈</h1>
        </div>
    """.format(logo_image)

    st.markdown(header_html, unsafe_allow_html=True)



    # st.header("Future Stock Price Prediction \U0001F4C8")
    # Model selector
    model_option = st.selectbox(
        'Please Select Your Model',
        ('LSTM', 'ARIMA'),
        key="model_option",

    )
    
    # For Data selection
    data_option = st.radio('Select the Data Type', ["NASDAQ", "S&P"], horizontal=True)

    # For Week days selection
    weekdays = st.checkbox('Monday', 'Tuesday', 'Wednessday', 'Thursday', 'Friday')

    # Filter data based on high-impact news
    if high_impact_news:
        data = data[data['High_Impact_News'] == True]


    # set the tabs to navigate 
    tab1, tab2, tab3 = st.tabs(["Low/High Range", "Monday", "Misc"])
    # For tab1 content
    with tab1:
        st.write("Low and High Value Range")
        mydata = data.copy()
        mydata = mydata.set_index('Time')
        print(mydata.head())
        if model_option == 'LSTM':
            fig = forecast_high_low_lstm(mydata)
        if model_option == 'ARIMA':
            fig = arima(mydata)
        # Show the plot in Streamlit with zooming and panning enabled
        st.plotly_chart(fig, use_container_width=True, config={'scrollZoom': True})


    # For tab2 content
    with tab2:
        st.write("Monday")
        
    #For Tab3 content
    with tab3:
        data1 = data.copy()
        # Extract day of the week from Date
        data1['DayOfWeek'] = data1['Time'].dt.dayofweek
        # Calculate average close price  for each day of the week
        day_of_week_avg_yield = data1.groupby('DayOfWeek')['Close'].mean()

        # extract week of year
        data1['WeekOfYear'] = data1['Time'].dt.isocalendar().week
        # Calculate average yield for each week of the year
        week_of_year_avg_yield = data1.groupby('WeekOfYear')['Close'].mean()

        # Extract Month of the year
        data1['Month'] = data1['Time'].dt.month
        # Calculate average yield for each month of the year
        month_avg_yield = data1.groupby('Month')['Close'].mean()

        # Display average yield by day of the week
        st.subheader("Average Yield by Day of the Week")
        st.bar_chart(day_of_week_avg_yield)

        # Display average yield by week of the year
        st.subheader("Average Yield by Week of the Year")
        st.bar_chart(week_of_year_avg_yield)

        # Display average yield by month of the year
        st.subheader("Average Yield by Month of the Year")
        st.bar_chart(month_avg_yield)

        # Minimum and Maximum Yield
        min_yield = data['Close'].min()
        max_yield = data['Close'].max()

        st.subheader("Historical Minimum and Maximum Yield")
        st.write(f"Minimum Yield: {min_yield}")
        st.write(f"Maximum Yield: {max_yield}")

        # Display the DataFrame
        st.subheader("S&P 500 Data")
        st.write(data)


        

if __name__ == '__main__':
    main()