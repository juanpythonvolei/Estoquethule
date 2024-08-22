
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
import requests
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
tab1,tab2 = st.tabs(['Alimentação Manual','Alimentação de itens da nota'])
with tab1:
  item = st.selectbox(label='',palceholder='Insira um item',options=['vazio'])
  quantidade = st.number_input(placeholder=f'Insira a quantidade do item: {item}',value=None,label='')
  if item and quantidade:
    st.button(f'Adicionar Item: {item}')
  
