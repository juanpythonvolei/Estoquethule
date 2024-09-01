import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
import requests
import random
import xmltodict
from datetime import datetime
barra_lateral = st.sidebar.selectbox('Selecione uma aba',['Faturamento','Mercado','Separação'])
ref_faturamento = db.reference('Faturamento')
numero_processo = 0
data_hora_atual = datetime.now()
data_atual = data_hora_atual.strftime("%d-%m-%Y")
if barra_lateral == 'Faturamento':
              numero_processo +=1
              lista_filtrada = []         
              uploaded_files = st.file_uploader("Escolha os arquivos", type=[f'xml'], accept_multiple_files=True)
              lista = []   
              contagem = 0    
              erro = 0  
              valor = 0
              if uploaded_files:
                        for nota in uploaded_files:
                          try:
                                              
                                              xml_data = nota.read()
                                              documento = xmltodict.parse(xml_data)
                                              codigo_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['cProd']
                                              descricao_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['xProd']       
                                              quantidade_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['qCom'] 
                                              valor_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['vProd']
                                              cliente = documento['nfeProc']['NFe']['infNFe']['dest']['xNome']
                                              numero_da_nota = documento['nfeProc']['NFe']['infNFe']['ide']['nNF']
                                              data_emit = documento['nfeProc']['NFe']['infNFe']['ide']['dhEmi'][:10]
                                              caminho_faturamento = f'{data_atual}/{numero_da_nota}'
                                              dict_pedido = {'cliente':cliente,'produtos':f'Produto:{codigo_produto} - Valor:{valor_produto}','descrição do produto':descricao_produto,'quantidade':quantidade_produto,'processo':numero_processo,'Data':data_emit,'numero da nota':numero_da_nota}
                                              ref_faturamento.child(caminho_faturamento).set(dict_pedido)
                                              contagem += 1
                          except:     
                             erro += 1
                        st.metric(label='Total de notas processadas',value=contagem)
                        st.metric(label='Total de notas não processadas',value=erro)
elif barra_lateral ==  'Mercado':
  lista_processos = []
  requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
  roteiro = requiscao.json()
  dados = roteiro['Faturamento']
  for item in dados:
    notas = dados[f'{item}']
    for item in notas:
      info = notas[f'{item}']
      numero_processo = info['processo']
      if numero_processo in lista_processos:
        pass
      else:
        lista_processos.append(numero_processo)
  selecao = st.selectbox(label='',palceholder='selecione o Processo',options = lista_processos,index=None)
