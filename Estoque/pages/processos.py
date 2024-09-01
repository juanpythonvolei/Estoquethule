import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
import requests
barra_lateral = st.sidebar.selectbox('selecione uma aba',['faturamento','mercado','separação'])

