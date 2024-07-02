import os
import streamlit as st
from groq_client import get_chat_completion
from config import load_config
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import groq
from pandasql import sqldf

# Load the environment variables
load_config()

user_input = st.chat_input('start typing')

if not user_input: 
    st.title('Hello there 👋')

if user_input:
    model_choice = st.sidebar.selectbox('Choose Model', ('LLaMA3 70b', 'Mixtral 8x7b', 'Gemma 7b'))

    model_map = {
        'LLaMA3 70b': 'llama3-70b-8192',
        'Mixtral 8x7b': 'mixtral-8x7b-32768',
        'Gemma 7b': 'gemma-7b-it'
    }

    model = model_map.get(model_choice, 'llama3-70b-8192')

    prompt = f"""
    Consider the Schema of the Tables, which contains the following information:
    Table1: encash_df (This table contains the information, when the political party encashed the Bond amount)
    Columns: date_of_encashment INT, month_of_encashment INT, year_of_encashment INT, name_of_political_party VARCHAR(255), bond_number INT, denominations DECIMAL(15, 2)

    Table2: purchase_df (This table contains the information, when the purchaser by the Bond amount)
    Columns: date_of_purchase INT, month_of_purchase INT, year_of_purchase INT, name_of_purchaser VARCHAR(255), bond_number INT, denominations DECIMAL(15, 2)

    Both tables can be combined on same column, which is bond_number.

    Convert the following natural language query to an SQL query on the basis of above table:
    "{user_input}"

    Provide only the SQL query as the output, without any additional explanations and don't add \.
    """

    # Call the GROQ API
    response = get_chat_completion(
        prompt,
        model  # or another appropriate GROQ model
    )

    sql_query = response

    Encasher = pd.read_csv('Encasher.csv')
    Purchaser = pd.read_csv('Purchaser.csv')
    encash_df  = Encasher.copy()
    purchase_df = Purchaser.copy()

    # Dictionary to map month abbreviations to numbers
    month_map = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
        'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }

    # Split the date_of_encashment column
    encash_df[['date_of_encashment', 'month_of_encashment', 'year_of_encashment']] = encash_df['date_of_encashment'].str.split('-', expand=True)

    # Convert month abbreviations to numbers
    encash_df['month_of_encashment'] = encash_df['month_of_encashment'].map(month_map)

    # Ensure all columns are of integer type
    encash_df['date_of_encashment'] = encash_df['date_of_encashment'].astype(int)
    encash_df['month_of_encashment'] = encash_df['month_of_encashment'].astype(int)
    encash_df['year_of_encashment'] = encash_df['year_of_encashment'].astype(int)
    encash_df['year_of_encashment'] = encash_df['year_of_encashment'] + 2000

    encash_df['bond_number'] = encash_df['bond_number'].astype(int)
    encash_df['denominations'] = encash_df['denominations'].astype(int)

    month_map = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
        'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }

    # Split the date_of_purchase column
    purchase_df[['date_of_purchase', 'month_of_purchase', 'year_of_purchase']] = purchase_df['date_of_purchase'].str.split('-', expand=True)

    # Convert month abbreviations to numbers
    purchase_df['month_of_purchase'] = purchase_df['month_of_purchase'].map(month_map)

    # Ensure all columns are of integer type
    purchase_df['date_of_purchase'] = purchase_df['date_of_purchase'].astype(int)
    purchase_df['month_of_purchase'] = purchase_df['month_of_purchase'].astype(int)
    purchase_df['year_of_purchase'] = purchase_df['year_of_purchase'].astype(int)
    purchase_df['year_of_purchase'] = purchase_df['year_of_purchase'] + 2000

    purchase_df['bond_number'] = purchase_df['bond_number'].astype(int)
    purchase_df['denominations'] = purchase_df['denominations'].replace(',', '', regex=True).astype(int)

    pysqldf = lambda q: sqldf(q, globals())

    query = sql_query

    result_df = pysqldf(query)
    answer=result_df.iloc[0, 0]

    st.write(user_input)
    st.write(answer)