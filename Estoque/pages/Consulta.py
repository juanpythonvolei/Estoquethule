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
produtos = st.selectbox(label='',placeholder='Selecione o Produto',options=lista_produtos,index=None)
descricao_visual = st.container()
if produtos:
  
  texto=''
  lista_foto = []
  for item in dados:
                quantidade2 = 0  
                item_estoque = dados[f'{item}']
                for elemento in item_estoque:
                    espec = item_estoque[f'{elemento}']
                    codigo = espec['Código']
                    if codigo == produtos:
                      
                      codigo = espec['Código']
                      descricao = espec['Descrição']
                      quantidade = espec['Quantidade']
                      quantidade2 += quantidade
                      foto = espec['Foto']
                      localizacao = espec['localicação']
                      if foto in lista_foto:
                        pass
                      else:
                        lista_foto.append(foto)
                        
                      localizacao_atual = espec['localicação']
                if quantidade2 > 0:   
                  texto += f'Produto {produtos} possui: {quantidade2} unidades na posição {localizacao} do depósito: Revenda  \n'
                else:
                  texto += ''
  with descricao_visual:
      foto = st.image(lista_foto[0])
      st.info(texto)

