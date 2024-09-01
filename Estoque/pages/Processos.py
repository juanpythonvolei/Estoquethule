import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
import requests
import random
import xmltodict
barra_lateral = st.sidebar.selectbox('Selecione uma aba',['Faturamento','Mercado','Separação'])
ref_faturamento = db.reference('Faturamento')

if barra_lateral == 'Faturamento':
              numero_processo = random.randint(1,10000)
              caminho_faturamento = f'{numero_processo}'
              lista_filtrada = []         
              uploaded_files = st.file_uploader("Escolha os arquivos", type=[f'xml'], accept_multiple_files=True)
              lista = []   
              contagem = 0    
              erro = 0  
              valor = 0  
              if uploaded_files:
                        for nota in uploaded_files:
                  
                                              xml_data = nota.read()
                                              documento = xmltodict.parse(xml_data)
                                              codigo_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['cProd']
                                              descricao_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['xProd']       
                                              quantidade_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['qCom']  
                                              valor_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['vProd']
                                              cliente = documento['nfeProc']['NFe']['infNFe']['emit']
                                              #numero_da_nota = documento['nfeProc']['NFe']['infNFe']['nNF']
                                              data_emit = documento['nfeProc']['NFe']['infNFe']['dhEmi']
                                              dict_pedido = {'cliente':cliente,'produtos':f'{codigo_produto} - {valor_produto}','descrição do produto':descricao_produto,'quantidade':quantidade_produto,'numero da nota':numero_da_nota,'processo':processo}
                                              ref_faturamento.child(caminho_faturamento).set(dict_pedido)
                                              contagem += 1
 
                        st.metric(label='Total de notas processadas',value=contagem)
                        st.metric(label='Total de notas não processadas',value=erro)
                                                  

