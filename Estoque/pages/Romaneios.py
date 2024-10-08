
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
import requests
import random
import xmltodict
from datetime import datetime
import pandas as pd



image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requiscao.json()
ref_faturamento = db.reference('Faturamento')
ref_mercado = db.reference('mercado')  
ref_romaneios = db.reference('romaneios') 
data_hora_atual = datetime.now()
data_atual = data_hora_atual.strftime("%d-%m-%Y")
data_romaneio = st.date_input(label='Selecione uma data',value=None)
ano = str(data_romaneio)[0:4]
mes = str(data_romaneio)[5:7]
dia = str(data_romaneio)[8:] 
data_romaneio = f'{dia}-{mes}-{ano}' 
col1,col2,col2 = st.columns(3)
lista_transps = []
separacoes = roteiro['separacao']
for item in separacoes:
      if item == data_romaneio:
            for x in separacoes[f'{item}']:
                  lista_transps.append(x)
if data_romaneio:
  with col1:
    transp  = st.selectbox(label='',placeholder='Selecione uma transportadora',options=lista_transps,index=None)      
  with col2:
    if transp:  
              lista = []        
              romaneio_criado = False
              i = 0  
              for item in roteiro['romaneios']:
                              if item == data_romaneio:
                                    verifs = roteiro['romaneios'][f'{item}']
                                    for verif in verifs:
                                          if verif == transp:
                                                romaneio_criado = True
                                                processo  = verifs[f'{verif}']
                                                for y in processo:
                                                      dict_processo  = {'numero':y}
                                                      for z in processo[f'{y}']:
                                                            lista.append(z)
                                                            
                                                
                                                 
              if romaneio_criado == True:
                              st.info(f'Já existe um Romaneio {dict_processo['numero']} para essa transportadora na data selecionada')
                              adicionar_ao_romaneio = st.popover("Adicionar itens ao romaneio")
                              ver_romaneio = st.popover("Vizualizar romaneio")  
                              with adicionar_ao_romaneio:
                                    nota = st.text_input(label='',placeholder='Insira o número da nota')
                                    produto = st.text_input(label='',placeholder='Insira o código do produto')
                                    quantidade = st.text_input(label='',placeholder='Insira a quantidade')
                                    if nota and produto and quantidade:
                                          adicao = {'Nota': nota, 'Transportadora': transp[:6], 'itens': quantidade}
                                          lista.append(adicao)
                                          ref_romaneios.child(f'{data_romaneio}/{transp}/{dict_processo['numero']}').set(lista)
                              with ver_romaneio:
                                     lista_nova = []
                                     
                                     for item in lista:
                                           texto = f'Transportadora : {item[f'Transportadora']}\n Cliente: {item['Cliente']}\n Nota: {item['Nota']}\n Itens: {item['itens']}'
                                           lista_nova.append(texto)
                                     dict_exibir = {'Romaneio':lista_nova}
                                     df_novo = pd.DataFrame(dict_exibir)
                                     st.table(df_novo)            
                                
              else:
                                            botao_romaneios = st.button('Criar Romaneio')
                                            if botao_romaneios:  
                                                  lista_romaneios = []
                                                  for data_separacao in separacoes:
                                                        if data_separacao == data_romaneio:
                                                              transps = separacoes[f'{data_separacao}']
                                                              for elemento in transps:
                                                                    if elemento == transp[:6]:
                                                                        notas = transps[f'{elemento}']
                                                                        for nota in notas:
                                                                              i += 1
                                                                              volumes = notas[f'{nota}']['volumes']
                                                                              clientes = notas[f'{nota}']['cliente']
                                                                              a = notas[f'{nota}']['nota']
                                                                              texto = {'Nota': a,  
                                                                              'Cliente': clientes,
                                                                              'Transportadora': transp[:6],
                                                                              'itens': volumes}
                                                                              lista_romaneios.append(texto)
                              
                                                  numero_romaneio = random.randint(10,10000)
                                                  dict_romaneios = {f'pedidos do romaneio {numero_romaneio}':lista_romaneios} 
                                                  df = pd.DataFrame(dict_romaneios)
                                                  st.table(df)
                                                  ref_romaneios.child(f'{data_romaneio}/{transp}/{numero_romaneio}').set(lista_romaneios)
                                                  st.success('Romaneio criado com sucesso')
                                                

                          
              
  
        
