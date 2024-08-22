import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
import requests
st.write('Não está funcionando')
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
col1,col2,col3 = st.columns(3)
with col1:
  deposito_origem = st.selectbox(index=None,label='',placeholder='depósito de origem',options=['Rev','Dev','Rec','Ele'])
with col2:
  deposito_final= st.selectbox(index=None,label='',placeholder='depósito de origem',options=['Rev'])
if deposito_origem and deposito_final:
  if deposito_origem == 'Rec' or deposito_origem == 'Dev'or deposito_origem == 'Ele':
    origem = st.text_input(label='',placeholder='Insira a posição de Origem',value=deposito_origem)
  else:
    origem = st.text_input(label='',placeholder='Insira a posição de Origem')
    colum2=origem [3:6]
    Prat2=origem [0:2]
    alt2 = origem [7:]
    if len(colum2) != 3 or len(alt2)!= 2 or len(Prat2)!=2:
        st.error(f'A posição {origem} está incorreta. Insira-a novamente')
        localizacao = ''
  produto = st.text_input(label='',placeholder='Insira o produto')
  if produto:
    st.info(produto)
    quantidade = st.text_input(label='',placeholder='Insira a quantidade')
    final = st.text_input(label='',placeholder='Insira a posição Final')
    if final:
      colum=final[3:6]
      Prat=final[0:2]
      alt = final[7:]
      if len(colum) != 3 or len(alt)!= 2 or len(Prat)!=2:
            st.error(f'A posição {final} está incorreta. Insira-a novamente')
            localizacao = ''
    
    if origem and produto and quantidade and final:
      botao_tranferir = st.button(f'Transferir {produto}')
    else:
      st.error('Ainda há campos a serem preenchidos')
    if botao_transferir:
      if deposito_origem == 'Rec':
        requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
        roteiro = requiscao.json()
        dados = roteiro['Depósito']
        quantidade_atual = dados['Rec'][f'{}']
        deposito_ref = db.reference('Depósito')
        caminho_rec = f'Rec/quantidade'
        nova_quantidade = quantidade
        deposito_ref.child(caminho_rec).set(nova_quantidade)
        caminho_rev = f'Rev/{localizacao}'
        deposito_ref.child(caminho_rev).set({
        'Produto': 'disponível',
        'quantidade': 100  # Exemplo de dado adicional
    })
