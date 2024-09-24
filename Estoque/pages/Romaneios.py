
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
requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requiscao.json()
ref_faturamento = db.reference('Faturamento')
ref_mercado = db.reference('mercado')  
ref_romaneio = db.reference('romaneios') 
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
            nome = str(separacoes[f'{item}'].keys())
            nome = nome.replace('dict_keys','')
            nome = nome.replace('[','')
            nome = nome.replace(']','')
            nome = nome.replace('(','')
            nome = nome.replace(')','')
            nome = nome.replace("'","")
            lista_transps.append(nome)
if data_romaneio:
  with col1:
    transp  = st.selectbox(label='',placeholder='Selecione uma transportadora',options=lista_transps,index=None)      
    if transp:  
              i = 0  
              botao_romaneios = st.button('Criar Romaneio')
              if botao_romaneios:  
                    dict_romaneios = {}
                    lista_romaneios = []
                    for data_separacao in separacoes:
                          if data_separacao == data_romaneio:
                                transps = separacoes[f'{data_separacao}']
                                for elemento in transps:
                                      if elemento == transp[:6]:
                                          nome_nota = str(transps[f'{elemento}'].keys())
                                          nome_nota = nome_nota.replace('dict_keys','')
                                          nome_nota = nome_nota.replace('[','')
                                          nome_nota = nome_nota.replace(']','')
                                          nome_nota = nome_nota.replace('(','')
                                          nome_nota = nome_nota.replace(')','')
                                          nome_nota = nome_nota.replace("'","")  
                                          notas = transps[f'{elemento}']
                                          for nota in notas:
                                                i += 1
                                                volumes = notas[f'{nota}']['volumes']
                                                clientes = notas[f'{nota}']['cliente']
                                                a = notas[f'{nota}']['nota']
                                                texto s= f' Nota: {a}  Cliente: {clientes}  Transportadora: {transp[:6]} itens: {volumes}'
                                                dict_romaneios.update({f'{i}':texto})
                     
                    st.write(dict_romaneios)                            
                                                

                          
              #if botao_romaneios:
                  #try:
                        #for item in roteiro['romaneios']:
                              #if item == data_romaneio:
                                    #romaneios = data_romaneio[f'{item}']
                                    #for romaneio in romaneios:
                                          #numero_romaneio = romaneios[f'{romaneio}']['numero']
  
        
