import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
import requests
from streamlit_option_menu import option_menu
from ia import consulta_de_itens_e_posicoes
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requiscao.json()
dados3 = roteiro['Depósito']['Rec']
dados = roteiro['Depósito']['Rev']
dados2 = roteiro['Estoque']
quantidade = 0
menu = option_menu('selecione uma opção',['Consultar item','consultar posição'])
col1,col2,col3 = st.columns(3)
if menu == 'Consultar item':
 
  texto_item = ''
  lista_itens = [elemento for elemento in dados2]
  with col1:
   selecao_item = st.selectbox(label = '',placeholder='Selecione um Item',options=lista_itens,index=None)
   if selecao_item:
    item_rec = dados3[f'{selecao_item}']['quantidade']
    foto = dados2[f'{selecao_item}'][f'foto']
    st.warning(f'O item {selecao_item} possúi {item_rec} unidades em Rec')
    for item in dados:
      posicao = dados[f'{item}']
      for produto in posicao:
        if produto == selecao_item:
           quantidade = posicao[f'{produto}']['quantidade']
           info =  f'''
           O item {selecao_item} possúi {quantidade} unidades na posição {item}
           '''
           texto_item += info
    st.info(texto_item) 
    st.image(foto)
   with col2:
    with st.popover('🤖'):

elif menu == "consultar posição":
  texto_posicao =''
  lista_posicoes = [elemento for elemento in dados]
  selecao_posicao = st.selectbox(label = '',placeholder='Selecione uma posição',options=lista_posicoes,index=None)
  if selecao_posicao:
   for item in dados:
     if item == selecao_posicao:
      posicao = dados[f'{item}']
      for produto in posicao:
        ativo = produto
        quantidade = posicao[f'{produto}']['quantidade']
        informacao = f'''
        {ativo}-{quantidade} unidades
        
        '''
        texto_posicao += informacao
   st.info( f'''
   A posição {selecao_posicao} possúi os segunites itens
              
             {texto_posicao}
                                '''
)
