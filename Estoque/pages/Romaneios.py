
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
import requests
import random
import xmltodict
from datetime import datetime
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requiscao.json()
ref_faturamento = db.reference('Faturamento')
ref_mercado = db.reference('mercado')  
data_hora_atual = datetime.now()
data_atual = data_hora_atual.strftime("%d-%m-%Y")
data_romaneio = st.date_input(label='Selecione uma data',value=None)
ano = str(data_romaneio)[0:4]
mes = str(data_romaneio)[5:7]
dia = str(data_romaneio)[8:] 
data_romaneio = f'{dia}-{mes}-{ano}' 
col1,col2,col2 = st.columns(3)
lista_transps = []
separacoes = roteiro['separacao']
for item in separacoes:
      if item == data_romaneio:
            lista_transps.append(separacoes[f'{item}'].keys())
if data_romaneio:
  with col1:
    transp  = st.selectbox(label='',placeholder='Selecione uma transportadora',options=lista_transps)
    
  
        
