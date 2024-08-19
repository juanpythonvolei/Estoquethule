import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
import requests
col1,col2,col3 = st.columns(3)
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
with col1:
  deposito_origem = st.selecbox(index=None,label='',placeholder='Selecione o depósito de origem',options=['Rev','Dev','Rec','Ele'])
with col2:
  deposito_final= st.selecbox(index=None,label='',placeholder='Selecione o depósito de origem',options=['Rev'])
if deposito_origem and deposito_final:
  Origem = st.text_input(label='',palceholder='Insira a posição de Origem')
  produto = st.text_input(label='',placeholder='Insira o produto')
  produto = st.text_input(label='',placeholder='Insira a quantidade')
  produto = st.text_input(label='',placeholder='Insira a posição Final')
