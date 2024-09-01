import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
import requests
barra_lateral = st.sidebar.selectbox('Selecione uma aba',['Faturamento','Mercado','Separação'])
if barra_lateral == 'Faturamento':
  

