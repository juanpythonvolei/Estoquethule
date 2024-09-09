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
lista_numero_processo = []
requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requiscao.json()
ref_faturamento = db.reference('Faturamento')
ref_mercado = db.reference('mercado')  
ref_estoque =db.reference('Depósito')
data_hora_atual = datetime.now()
data_atual = data_hora_atual.strftime("%d-%m-%Y")
caminho_faturamento = f'{data_atual}'
#ref_faturamento.child(caminho_faturamento).set('a')
dados = roteiro['Faturamento']
dados2 = roteiro['Depósito']['Rev'] 
try:
  dados4 = roteiro['mercado']
except:
  dados4 = None
try:
  dados5 = roteiro['separacao']
except:
  dados5 = None

lista_filtrada = []         
uploaded_files = st.file_uploader("Escolha os arquivos", type=[f'xml'], accept_multiple_files=True)
lista = []   
contagem = 0    
erro = 0  
valor = 0
nao_rev = []
lista_ver = []
lista_mais = []
if uploaded_files:
                        for nota in uploaded_files:
                          
                                             
                                              xml_data = nota.read()
                                              documento = xmltodict.parse(xml_data)
                                              try:
                                                codigo_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['cProd']
                                                numero_da_nota = documento['nfeProc']['NFe']['infNFe']['ide']['nNF']
                                                descricao_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['xProd']
                                                transportadora = documento['nfeProc']['NFe']['infNFe']['transp']['transporta']['xNome']
                                                quantidade_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['qCom'] 
                                                valor_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['vProd']
                                                cliente = documento['nfeProc']['NFe']['infNFe']['dest']['xNome']
                                                caminho_faturamento = f'{data_atual}/{numero_da_nota}'
                                                data_emit = documento['nfeProc']['NFe']['infNFe']['ide']['dhEmi'][:10]
                                                for posicao in dados2:
                                                  itens_posicao = dados2[f'{posicao}']
                                                  for item in itens_posicao:
                                                    try:
                                                      if str(item) == str(codigo_produto):
                                                        lista_ver.append(
                                                          {
                                                           'produto':item,
                                                           'nota':numero_da_nota,
                                                           'descricao': descricao_produto,
                                                           'quantidade': quantidade_produto,
                                                           'cliente':cliente,
                                                           'valor':valor_produto,
                                                           'data':data_emit ,
                                                           'transportadora':transportadora 
                                                           
                                                          
                                                            }
                                                                         )
                                                      else:
                                                          nao_rev +=1
                                                    except:
                                                      pass
                                              except:
                                                produtos_excessao = documento['nfeProc']['NFe']['infNFe']['det']
                                                for produto in produtos_excessao:
                                                 try:
                                                  codigo_produto = produto['prod']['cProd']
                                                  descricao_produto = produto['prod']['xProd']       
                                                  quantidade_produto = produto['prod']['qCom'] 
                                                  valor_produto = produto['prod']['vProd']
                                                  cliente = documento['nfeProc']['NFe']['infNFe']['dest']['xNome']
                                                  transportadora = documento['nfeProc']['NFe']['infNFe']['transp']['transporta']['xNome']
                                                  numero_da_nota = documento['nfeProc']['NFe']['infNFe']['ide']['nNF']
                                                  
                                                  descricao_produto = produto['prod']['xProd']
                                                  for posicao in dados2:
                                                    itens_posicao = dados2[f'{posicao}']
                                                    for item in itens_posicao:
                                                      
                                                        if str(item) == str(codigo_produto):
                                                          lista_ver.append(
                                                            {
                                                             'produto':item,
                                                             'nota':numero_da_nota,
                                                             'descricao': descricao_produto,
                                                             'quantidade': quantidade_produto,
                                                             'cliente':cliente,
                                                             'valor':valor_produto,
                                                             'data':data_emit,
                                                             'transportadora':transportadora 
                                                             
                                                            
                                                           }
                                                                        )
                                                        else:
                                                            if f'{codigo_produto}/{numero_da_nota}' in nao_rev:
                                                              pass
                                                            else:
                                                              nao_rev.append(f'{codigo_produto}/{numero_da_nota}')
                                                 except:
                                                     pass
                                                
                                                
                                              
                                                     
                                                
                                                
                        if len(nao_rev) > 0:
                          lista_nao = []
                          for nao in nao_rev:
                            informacao = str(nao).split('/')
                            numero_nao = informacao[1]
                            lista_nao.append(numero_nao)
                        
                        lista_database = []
                        for pedido in lista_ver:
                          for posicaoo in dados2:
                            posicao = dados2[f'{posicaoo}']
                            for item in posicao:
                              carac = posicao[f'{item}']
                              if str(item) == str(pedido['produto']):
                                quantidade = carac[f'quantidade']
                                try:
                                  quantidade_pedido = str(pedido['quantidade'][0]).split('.')
                                except:
                                  pass
                                 
                                if float(quantidade) >= float(quantidade_pedido[0]):
                                  info = f'{pedido['produto']}/{posicaoo}/{pedido['quantidade'][0]}'
                                  if str(pedido['produto']) == str(item):
                                    lista_database.append(pedido['produto'])
                                    qtd_final = float(quantidade) - float(quantidade_pedido[0])
                                    st.write(qtd_final)
                                    st.write(pedido['produto'])
                                    if dados2[f'{posicaoo}'][f'{pedido['produto']}']['quantidade'] > 0:
                                      ref_estoque.child(f'Rev/{posicaoo}/{pedido['produto']}/quantidade').set(qtd_final)
                                      requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
                                      roteiro = requiscao.json()
                                      dados2 = roteiro['Depósito']['Rev']
                                    else:
                                      pass  
                                  else:
                                    pass
                                  pedido.update({'posicao':posicaoo})
                                  contagem +=1
                                  
                                  
                        st.write(lista_database) 
                        st.write(lista_ver)
                        caminho_faturamento = f'{data_atual}/{random.randint(10,1000)}'
                        ref_faturamento.child(caminho_faturamento).set(lista_ver)
                        st.metric(label='Notas faturadas',value=contagem)
                        st.metric(label='Produtos não estocados',value=len(list(set(nao_rev))))
                        if len(nao_rev) > 0:
                          st.metric(label='Notas não Faturadas',value=len(list(set(lista_nao))))
                 
                          
                                
                                             
                                                                 
         
