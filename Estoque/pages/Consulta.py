import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
import requests
from streamlit_option_menu import option_menu
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requiscao.json()
dados = roteiro['Depósito']['Rev']
dados2 = roteiro['Estoque']
quantidade = 0
menu = option_menu('selecione uma opção',['Consultar item','consultar posição'])
if menu == 'Consultar item':
  texto_item = ''
  lista_itens = [elemento for elemento in dados2]
  selecao_item = st.selectbox(label = '',placeholder='Selecione um Item',options=lista_itens,index=None)
  for item in dados:
    posicao = dados[f'{item}']
    for produto in posicao:
      if produto == selecao_item:
         st.write(posicao[f'{produto}'])
elif menu == "consultar posição":
  lista_posicoes = [elemento for elemento in dados]
  selecao_posicao = st.selectbox(label = '',placeholder='Selecione um Item',options=lista_posicoes,index=None)
