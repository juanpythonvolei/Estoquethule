
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
import requests
import xmltodict
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requiscao.json()
dados2 = roteiro['Depósito']['Rec']
ref_cadastro = db.reference('Estoque')
ref_rec = db.reference('Depósito')
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
      quantidade_atual_rec = dados2[f'{item}']['quantidade']  
      quantidade = st.number_input(placeholder=f'Insira a quantidade do item',value=None,label='')
      if item and quantidade:
        adicionar = quantidade + quantidade_atual_rec
        botao_adicionar = st.button(f'Adicionar Item: {item}')
        if botao_adicionar:
          if item not in lista_produtos:
            alerta(item)  
          else:  
              deposito_ref = db.reference('Depósito')
              caminho = f'Rec/{item}'
            
            # Adicionando dados
              deposito_ref.child(caminho).set({
                  'quantidade': adicionar  # Exemplo de dado adicional
              })
              st.success(f'Item {item} adicionado com sucesso')
    with tab2:
          lista_filtrada = []   
          tipo_arquivo = st.selectbox(label='',placeholder='Selecione o tipo de arquivo de cadastro automático',options=['xml','xlsx','csv'],index=None) 
          if tipo_arquivo:  
              uploaded_files = st.file_uploader("Escolha os arquivos", type=[f'{tipo_arquivo}'], accept_multiple_files=True)
              lista = []   
              contagem = 0    
              erro = 0  
              valor = 0  
              for item in dados:
                  if item not in lista:
                      lista.append(item)
                  else:
                      pass
              if uploaded_files:
                        for nota in uploaded_files:
                                          try:  
                                              xml_data = nota.read()
                                              documento = xmltodict.parse(xml_data)
                                              codigo_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['cProd']
                                              codigo_ean = documento['nfeProc']['NFe']['infNFe']['det']['prod']['cEAN']
                                          except:
                                              pass
                                          if codigo_produto in lista:
                                              pass
                                          else:  
                                              try:
                                                  descricao_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['xProd']   
                                                  ean_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['cEAN']     
                                                  dict_produto={'Foto':'','Descrição':descricao_produto,'EAN':codigo_ean}
                                                  quantidade_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['qCom']  
                                                  valor_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['vProd']
                                                  valor += float(valor_produto)
                                                  if '.' in quantidade_produto:
                                                      numero,excesso = quantidade_produto.split('.')
                                                      quantidade_produto = numero
                                                  caminho_cadastro = f'{codigo_produto}'
                                                  caminho_rec = f'Rec/{codigo_produto}'
                                                  ref_cadastro.child(caminho_cadastro).set(dict_produto)
                                                  dict_rec = {'quantidade':int(quantidade_produto)}
                                                  ref_rec.child(caminho_rec).set(dict_rec)
                                                  contagem += 1
                                              except:
                                                  erro += 1
                                                  pass
                        col1,col2,col3 = st.columns(3)
                        with col1:  
                            st.metric(label='Total de itens cadastrados',value=contagem)
                        with col2:
                            st.metric(label='Total de itens não possíveis de cadastrar',value=erro)
                        with col3:
                            st.metric(label='Valor Total dos itens cadastrados',value=f'{valor} R$')
                        st.success(f'Processo Concluído')    

else:
    st.error('Não há estoque diponível')
      
