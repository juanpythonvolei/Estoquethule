
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
import requests
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requiscao.json()
ref_cadastro = db.reference('Estoque')
if 'Estoque' in roteiro:
    dados = roteiro['Estoque']
    @st.dialog(f"Atenção") 
    def alerta(item):
        st.warning(f'O item: {item} não conta no cadastro')
        descricao = st.text_input(label='',placeholder='Insira uma descrição')
        if descricao:  
              deposito_ref = db.reference('Depósito')
              caminho = f'Rec/{item}'
              
              Estoque_ref = db.reference('Estoque')
              caminho_estoque = f'{item}'
            
            # Adicionando dados
              deposito_ref.child(caminho).set({
                  'quantidade': quantidade  # Exemplo de dado adicional
              })
              Estoque_ref.child(caminho_estoque).set({
                  'Descrição': descricao,
                  'foto':''# Exemplo de dado adicional
              })
              st.success(f'O {item} foi adicionado em {quantidade} unidades e cadastrado com sucesso')
    lista_produtos = []
    coletor = st.toggle('Coletor') 
    for item in dados:
                    if item in lista_produtos:
                          pass
                    else:
                          lista_produtos.append(item)
    tab1,tab2 = st.tabs(['Alimentação Manual','Alimentação de itens da nota'])
    
    with tab1:
      if coletor:  
          item = st.text_input(label='',placeholder='Insira um item')  
      else:
          item = st.selectbox(label='',placeholder='Insira um item',index=None,options=lista_produtos)
      quantidade = st.number_input(placeholder=f'Insira a quantidade do item',value=None,label='')
      if item and quantidade:
        botao_adicionar = st.button(f'Adicionar Item: {item}')
        if botao_adicionar:
          if item not in lista_produtos:
            alerta(item)  
          else:  
              deposito_ref = db.reference('Depósito')
              caminho = f'Rec/{item}'
            
            # Adicionando dados
              deposito_ref.child(caminho).set({
                  'quantidade': quantidade  # Exemplo de dado adicional
              })
              st.success(f'Item {item} adicionado com sucesso')
    with tab2:
          lista_filtrada = []   
          tipo_arquivo = st.selectbox(label='',placeholder='Selecione o tipo de arquivo de cadastro automático',options=['xml','xlsx','csv'])   
          uploaded_files = st.file_uploader("Escolha os arquivos", type=[f'{tipo_arquivo}'], accept_multiple_files=True)
          lista = []   
          contagem = 0    
          for item in dados:
              if item not in lista:
                  lista.append(item)
              else:
                  pass
          if uploaded_files:
             try:
                    for nota in uploaded_files:
                                      xml_data = nota.read()
                                      documento = xmltodict.parse(xml_data)
                                      codigo_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['cProd']
                                      if codigo_produto in lista:
                                          pass
                                      else:  
                                          descricao_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['xProd']   
                                          ean_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['cEAN']     
                                          dict_produto={'Foto':'','Descrição':descricao_produt}
                                          caminho_cadastro = f'{codigo_produto}'
                                          ref_cadastro.child(caminho_cadastro).set(dict_produto)
                                          contagem += 1                      
                    st.success(f'{contagem} produtos foram cadastrados')    
              except:
                  pass
else:
    st.error('Não há estoque diponível')
      
