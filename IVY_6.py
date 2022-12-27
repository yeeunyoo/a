import streamlit as st 
import pandas as pd
import numpy as np
import pyodbc
import openpyxl
import sqlalchemy as sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from streamlit_autorefresh import st_autorefresh
from sqlalchemy.sql import text
from sqlalchemy import *
import sqlite3
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from st_aggrid import AgGrid
from st_aggrid import GridOptionsBuilder,GridUpdateMode, DataReturnMode
from deta import Deta
import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import win32com.client as win32
from streamlit_extras.switch_page_button import switch_page

# %%
st.set_page_config(layout="wide",initial_sidebar_state="collapsed")
st.markdown("<p style='text-align: center; color:#1428A0; font-size:40px; font-weight: bold; '>Salesman Account Change<br> Request Form 6</br></p>",unsafe_allow_html=True)
st.write("if you have any question, please contact IVY SOM team")
colA,colB, colC , coldD, colE= st.columns([3,3,3,2,2])
with colE:
    main_p=st.button(label="Go Back To Main Page")
    st.markdown(""" <style>
div.stButton > button:first-child {
    background-color: #ce1126;
    color: white;
    height: 3em;
    width: 12em;
    border-radius:10px;
    border:3px solid #000000;
    font-size:20px;
    font-weight: bold;
    margin: auto;
    display: block;
}</style>
""", unsafe_allow_html=True)
    if main_p:
        switch_page('Homepage')
server = '10.1.3.25' 
database = 'KIRA' 
username = 'kiradba' 
password = 'Kiss!234!' 
connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)
print("Connection Established:")

df=pd.read_sql('''
select distinct(salesteam_text) from [[dbo]].[TEMPORARY]]]
order by salesteam_text asc
''',con=engine)
# %%
cold1, cold2, cold3, cold4 = st.columns(4)
with cold1:
    st.subheader('Serial Number')
    st.write(st.session_state['Serial Number'])
with cold2:
    st.subheader("Requester's Name")
    st.write(st.session_state['Requester'])
with cold3:
    st.subheader('Start Date')
    d1 = st.date_input('Start Date', label_visibility='collapsed')
with cold4:
    st.subheader('End Date')
    d2 = st.date_input('End Date',label_visibility='collapsed')
col1_1, col1_2, col1_3, col1_4 = st.columns(4)
with col1_1:
    st.markdown("<p style = 'text-align: center;background-color:aquamarine; color:black; font-size:30px; margin-top:30px;font-weight:bold;'>New Person</p>", unsafe_allow_html=True)
with col1_2:
    st.subheader('Sales Team')
    st.write('Team '+st.session_state['IVY Sales Team 5'])
with col1_3:
    st.subheader('Sales Man')
    b = st.write(st.session_state['IVY Sales Man 5'])
with col1_4:
    st.subheader('Reason')
    reason = st.radio(label = ' ',options = ['Retiring', 'Moving to Another Account', 'New'], key = '37')
    
# %%
if reason != 'Retiring':
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.markdown("<p style = 'text-align: center;background-color:aquamarine;color:black; font-size:30px; margin-top:30px;font-weight:bold;'>Current Person</p>", unsafe_allow_html=True)
    with col6:
        AT_7 = st.selectbox('Sales Team', options = df, key = '2')
        st.session_state['IVY Sales Team 6'] = AT_7
        for i in st.session_state['IVY Sales Team 6']:
            new4 = ''.join(map(str,str(i)))
        st.session_state['IVY Sales Team 6'] = new4
    with col7:
        con = engine.connect()
        query3 = "select distinct(salesperson_text) from [[dbo]].[TEMPORARY]]] where salesdiv = 'div1' and salesteam_text = ?"
        df4 = con.execute(query3, AT_7)
        AS_7 = st.selectbox('Sales Man', options = df4, key = '3')
        st.session_state['IVY Sales Man 6'] = AS_7
    with col8:
        st.write(' ')
    # %%
    colA1, colA2 = st.columns(2)
    with colA1:
        with engine.connect() as conn:
            query4 = """WITH T1 as(select a.*, b.shiptoparty_dba,b.address,b.state_key, b.city from [[dbo]].[TEMPORARY]]] a left join [ivy.mm.dim.shiptoparty] b 
            on a.shiptoparty = b.shiptoparty) select DISTINCT(T1.shiptoparty), T1.shiptoparty_dba, T1.address,T1.state_key, T1.city from T1 
            where T1.salesdiv = 'div1' and T1.salesperson_text = ?"""
            qry = conn.execute(query4, AS_7)
            resultqry = []
            for row in qry:
                row_as_dict = row._mapping 
                row1 = row_as_dict.values()                                    
                resultqry.append(row1)
        st.header('Select Account')
        df2 = pd.DataFrame(list(resultqry), columns = ['Account Number','Account Name','Address','State','City'])
        gd = GridOptionsBuilder.from_dataframe(df2)
        gd.configure_pagination(enabled=True)
        gd.configure_default_column(enablePivot = True, enableValue = True, enableRowGroup = True)
        gd.configure_selection(selection_mode = 'multiple', use_checkbox=True)
        gd.configure_side_bar()
        gd.configure_column("Account Number", headerCheckboxSelection = True)
        gdOptions = gd.build()
        grid_Table = AgGrid(df2, gridOptions=gdOptions,data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
                            update_mode = GridUpdateMode.SELECTION_CHANGED,
                            height = 1000,
                            allow_unsafe_jscode=True,
                            theme='balham',
                            width=0.5
                                )
        sel_row = grid_Table["selected_rows"]
        trows = len(sel_row)
    with colA2:
        st.subheader(f'Total rows : {trows}')
        df = pd.DataFrame(sel_row, columns = ['Account Number','Account Name','State']) 
        st.header("Selected Account")  
        gd = GridOptionsBuilder.from_dataframe(df)
        gd.configure_pagination(paginationAutoPageSize=True)
        gd.configure_default_column(editable=True, groupable=True)
        grid_table2 = AgGrid(df,update_mode=GridUpdateMode.SELECTION_CHANGED,
                            height = 1000, allow_unsafe_jscode=True,width = 0.5,
                                theme='balham') 
        # %%
        # Create Result DataFrame to Send Email 
        num_row = len(df.index)
        df['From'] = str(st.session_state['IVY Sales Man 6'])
        df['To'] = str(st.session_state['IVY Sales Man 5'])
        df['Start_From'] = d1
        df['End_date'] = d2
        final = df[['From','To','Account Number','Account Name','State','Start_From','End_date']]
    # %%
    # Submit button Form
    with st.form('form 1'):
        st.write(final)
        button1 = st.form_submit_button('Submit')
        if button1:
            st.success('Your Request Has Been Submitted! ')
    with st.form('form 2'):
        button3 = st.form_submit_button('END')
        if button3:
            st.session_state.count+=1
            switch_page('FINAL')
    
# %%
if reason=='Retiring':
    d_f = st.date_input('Please Select Your Last Working Date: ')
    final = pd.DataFrame({'From':[st.session_state['IVY Sales Man 5']],'TO':['None'], 'Reason':['Retiring'], 'Last Date':[d_f]})
    with st.form('form 3'):
        button_1 = st.form_submit_button('Submit')
        if button_1:
            st.write(final)
            st.success('Your Request Has Been Submitted! ')
    with st.form('form 4'):
        button_2 = st.form_submit_button('End')
        if button_2:
            switch_page('FINAL')
