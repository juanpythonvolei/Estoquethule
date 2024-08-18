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
                    lista_produtos.append(codigo)
produtos = st.selectbox(label='',placeholder='Selecione o Produto',options=lista_produtos,index=None)
descricao_visual = st.container()
if produtos:
  quantidade2 = 0
  texto=''
  lista_foto = []
  for item in dados:
                item_estoque = dados[f'{item}']
                for elemento in item_estoque:
                    espec = item_estoque[f'{elemento}']
                    codigo = espec['Código']
                    if codigo == produtos:
                      codigo = espec['Código']
                      descricao = espec['Descrição']
                      quantidade = espec['Quantidade']
                      quantidade2+=quantidade
                      foto = espec['Foto']
                      if foto in lista_foto:
                        pass
                      else:
                        lista_foto.append(foto)
                        
                      localizacao = espec['localicação']
                      texto += f'''O Produto {codigo} possui: {quantidade} unidades na posição {localizacao} do depósito: Revenda
                      '''
  with descricao_visual:
      foto = st.image(lista_foto[0])
      st.info(texto)

