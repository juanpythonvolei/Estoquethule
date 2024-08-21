import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
import requests

image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
st.write('Está funcionando')
tab1,tab2 = st.tabs(['Alimentar Rec (Manual)','Iten em nota '])
with tab1:
  produto = st.selectbox(label='',placeholder='Selecione um Produto',['Opção'])
