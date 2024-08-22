
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
import requests
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requiscao.json()
dados = roteiro['Estoque']
lista_produtos = []
for item in dados:
                item_estoque = dados[f'{item}']
                for elemento in item_estoque:
                    espec = item_estoque[f'{elemento}']
                    codigo = espec['Código']
                    if codigo in lista_produtos:
                      pass
                    else:
                      lista_produtos.append(codigo)
tab1,tab2 = st.tabs(['Alimentação Manual','Alimentação de itens da nota'])
with tab1:
  item = st.selectbox(label='',placeholder='Insira um item',options=lista_produtos)
  quantidade = st.number_input(placeholder=f'Insira a quantidade do item: {item}',value=None,label='')
  if item and quantidade:
    botao_adicionar = st.button(f'Adicionar Item: {item}')
    if botao_adicionar:
      deposito_ref = db.reference('Depósito')
      caminho = f'Rec/{localizacao}'
    
    # Adicionando dados
      deposito_ref.child(caminho).set({
          'Produto': f'{item}',
          'quantidade': quantidade  # Exemplo de dado adicional
      })
  
