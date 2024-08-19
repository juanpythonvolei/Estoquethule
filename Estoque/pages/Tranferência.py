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
    origem = st.text_input(label='',placeholder='Insira a posição de Origem',value=deposito_origem)
else:
    origem = st.text_input(label='',placeholder='Insira a posição de Origem')
    col2=origem [3:6]
    Prat2=origem [0:2]
    alt2 = origem [7:]
    if len(col2) != 3 or len(alt2)!= 2 or len(Prat2)!=2:
        st.error(f'A posição {origem} está incorreta. Insira-a novamente')
        localizacao = ''
with col2:
  deposito_final= st.selectbox(index=None,label='',placeholder='depósito de origem',options=['Rev'])
if deposito_origem and deposito_final:

  produto = st.text_input(label='',placeholder='Insira o produto')
  quantidade = st.text_input(label='',placeholder='Insira a quantidade')
  final = st.text_input(label='',placeholder='Insira a posição Final')
  if produto:
    st.info(produto)
  if not origem or produto or quantidade or final:
    st.error('Atenção. Ainda há campos a serem preenchidos')
  else:
    st.button(f'Transferir {produto}')
    col=final[3:6]
    Prat=final[0:2]
    alt = final[7:]
    if len(col) != 3 or len(alt)!= 2 or len(Prat)!=2:
        st.error(f'A posição {final} está incorreta. Insira-a novamente')
        localizacao = ''
  
