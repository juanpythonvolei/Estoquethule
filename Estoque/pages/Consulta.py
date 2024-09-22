import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
from streamlit_option_menu import option_menu
import time
import google.generativeai as genai
import pandas as pd

GOOGLE_API_KEY = st.secrets['firebase']['GOOGLE_API_KEY']
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requiscao.json()
if 'Depósito' in roteiro:
     def consulta_itens_e_posicoes(a,b):
          response = chat.send_message(f'Você receberá a seguir um conjunto de dados relacionados a um estoque. Nessa base de dados, rec significa "recebimento" e se refere aos itens recebidos pela logística mas que, ainda não foram alocados no estoque. "rev" significa revenda e se refere aos itens que estão alocados no estoque físico. Por favor responda o que for possível conforme o solicitado. Segue a pergunta:{a}\n\n{b}\n')
          resposta = response.text
          st.chat_message.write(resposta) 
     dados3 = roteiro['Depósito']['Rec']
     dados = roteiro['Depósito']['Rev']
     dados2 = roteiro['Estoque']
     quantidade = 0
     col1,col2,col3 = st.tabs(['Consultar item','consultar posição','Assistente'])
     col4,col5,col6 = st.columns(3) 
     with col1:
          
       texto_item = ''
       lista_itens = [elemento for elemento in dados2]
       coletor = st.toggle('Coletor',key='posicao') 
       if coletor:
            selecao_item = st.text_input(label = '',placeholder='Insira o item')
       else:   
            selecao_item = st.selectbox(label = '',placeholder='Selecione um Item',options=lista_itens,index=None)   
       if selecao_item:   
         total_quantidade = 0
         total_posicoes = 0 
         item_rec = dados3[f'{selecao_item}']['quantidade']
         foto = dados2[f'{selecao_item}'][f'Foto']
         st.warning(f'O item {selecao_item} possúi {item_rec} unidades em Rec')
         for item in dados:
           posicao = dados[f'{item}']
           for produto in posicao:
             if produto == selecao_item:
                quantidade = posicao[f'{produto}']['quantidade']
                    
                if quantidade > 0:  
                     total_quantidade += quantidade
                     total_posicoes += 1
                     info =  f'''
                O item {selecao_item} possúi {quantidade} unidades na posição {item}
                '''
                     texto_item += info
                
                
             
                     
         st.info(texto_item)  
         try:   
              st.image(foto)    
         except:
              pass
         st.metric(label=f'Total unidades item {selecao_item}',value=total_quantidade)
         st.metric(label=f'Total posicoes para o item {selecao_item}',value=total_posicoes)    
     with col2:
       texto_posicao =''
       lista_posicoes = [elemento for elemento in dados]
       coletor = st.toggle('Coletor',key='localizacao')    
       if coletor:
            selecao_posicao = st.text_input(label = '',placeholder='Selecione uma posição')
       else:   
            selecao_posicao = st.selectbox(label = '',placeholder='Selecione uma posição',options=lista_posicoes,index=None)
       if selecao_posicao:
        for item in dados:
          if item == selecao_posicao:
           posicao = dados[f'{item}']
           for produto in posicao:
             ativo = produto
             quantidade = posicao[f'{produto}']['quantidade']
             informacao = f'''
             {ativo} -  {quantidade} unidades
             
             '''
             texto_posicao += informacao
        st.info( f'''
        A posição {selecao_posicao} possúi os segunites itens
                   
                  {texto_posicao}
                                     '''
     )
     with col3:
         texto_item = ''        
         for item in dados:
           posicao = dados[f'{item}']
           for produto in posicao:
                quantidade = posicao[f'{produto}']['quantidade']
                info =  f'''
                O item {produto} possúi {quantidade} unidades na posição {item}
                '''
                texto_item += info
         texto_posicao =''      
         for item in dados:         
                posicao = dados[f'{item}']
                for produto in posicao:
                  ativo = produto
                  quantidade = posicao[f'{produto}']['quantidade']
                  informacao = f'''
                  {ativo}-{quantidade} unidades
                  
                  '''
                  texto_posicao += informacao  
                texto_base = f'''
                  {texto_item}
               
                  {texto_posicao}
             '''              
         pergunta = st.chat_input()       
         if pergunta:         
                       consulta_itens_e_posicoes(pergunta,texto_base)          
else:
     st.error('Não há estoque disponível')
