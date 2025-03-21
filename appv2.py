import streamlit as st
import pandas as pd
import math
import joblib
from datetime import datetime
from sklearn.preprocessing import LabelEncoder
import os



port = os.environ.get('PORT', 8501)

st.title("CURRENCY PREDICTIONS")
st.subheader("V2.0.1")
st.write("##")
st.markdown('<span style="color:blue;">Make sure to use consistent data to get correct predictions.</span>', unsafe_allow_html=True)
#st.markdown('<span style="color:green;">Kenya Foreign Exchange Reserve is: 16023.8</span>', unsafe_allow_html=True)

st.write("---")

date_entry = None
date_entry = date_entry or datetime.now()

# Extraction of data from date input
def extract_date_features(date_entry):
    try:

        if isinstance(date_entry, str):
            date_entry = pd.to_datetime(date_entry)
    
        # Calculate the week of the month
        first_day_of_month = date_entry.replace(day=1)
        week_of_month = math.ceil((date_entry.day + first_day_of_month.weekday()) / 7)

        # Extract features
        features = {
            "year": date_entry.year,
            "Month": date_entry.month,
            "Quarter": (date_entry.month - 1) // 3 + 1,
            "Week-of-year": date_entry.isocalendar()[1],
            "Day-of-year": date_entry.timetuple().tm_yday,
            "Week-of-month": week_of_month,
            "Day-of-week": date_entry.weekday(),  # 0=Monday, 6=Sunday
        }

        return features
    except:
        st.write("Please input a valid data")







# Inputs
options = ['Yes', 'No']

date = st.date_input("Select a date that you would like to make prediction of:", None)
df = pd.DataFrame([extract_date_features(date)])

# Add more columns through input features
df['election-year'] = st.selectbox("Is the given date an election year in Kenya?", options)
df['US_election'] = st.selectbox("Is the given date an election year in United State of America?", options)

st.markdown('<span style="color:grey;">Click on the links provided to get factual data.</span>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("[Check US Interest Rate](https://fred.stlouisfed.org/series/DGS1)")

    df['Interest-rate'] = float(st.number_input("Enter the US Interest Rate."))
with col2:
    st.markdown("[Google Kenya Foreign Exchange Reserves](https://www.google.com/)")
    df['kenya_reserves'] = float(st.number_input("Enter Kenya Exchange Reserves."))


if st.button("Predict"):
    if (df['Interest-rate'] == 0).any():
        st.error("Interest Rate is NULL!!")
    else:    
        try:

            # Rearrange the features
            #df = df[["Interest-rate","Month","Quarter","Week-of-year","Week-of-month","Day-of-week","Day-of-year","election-year","US_election"]]
            



            
            label_encoder = LabelEncoder()
            df['election-year'] = df['election-year'].replace('Yes', 1)
            df['election-year'] = df['election-year'].replace('No', 0)
            df['US_election'] = df['US_election'].replace('Yes', 1)
            df['US_election'] = df['US_election'].replace('No', 0)
            df = df[["Interest-rate","Month","Quarter","Week-of-year","Week-of-month","Day-of-week","Day-of-year","election-year","kenya_reserves", "US_election"]]
            #st.dataframe(df)

            # Model
            model = joblib.load("randomforest.pkl")

            pred = model.predict(df)
            col1, col2 = st.columns(2)
            with col1:
              st.write("Currency Prediction is:" , pred)
            with col2:
              st.markdown("Accuracy:") 
              st.markdown("99.72594546924234%")
        except Exception as e:
            st.write(" error: ", e)
            # st.error("Step 1: Make sure, all data provided is correct,")
            # st.error("Step 2: If correct, Contact the Developer!")
                
 
