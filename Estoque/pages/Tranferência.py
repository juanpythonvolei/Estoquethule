import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
import requests

image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
col1,col2,col3 = st.columns(3)

with col1:
  deposito_origem = st.selectbox(index=None,label='',placeholder='depósito de origem',options=['Rev','Dev','Rec','Ele'])
if deposito_origem == 'Rec' or deposito_origem == 'Dev'or deposito_origem == 'Ele':
    Origem = st.text_input(label='',placeholder='Insira a posição de Origem',value=deposito_origem)
with col2:
  deposito_final= st.selectbox(index=None,label='',placeholder='depósito de origem',options=['Rev'])
if deposito_origem and deposito_final:
  Origem = st.text_input(label='',placeholder='Insira a posição de Origem')
  produto = st.text_input(label='',placeholder='Insira o produto')
  quantidade = st.text_input(label='',placeholder='Insira a quantidade')
  final = st.text_input(label='',placeholder='Insira a posição Final')
  if Produto:
    st.info(produto)
