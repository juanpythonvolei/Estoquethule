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
data_hora_atual = datetime.now()
data_atual = data_hora_atual.strftime("%d-%m-%Y")
caminho_faturamento = f'{data_atual}'
caminho_mercado = f'{data_atual}'
#ref_faturamento.child(caminho_faturamento).set('a')
#ref_mercado.child(caminho_mercado).set('a')
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

col7,col8,col9 = st.columns(3)
lista_ean = []
lista_processos = []
lista_datas =[]
lista_dicionarios = []  
requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requiscao.json()
dados = roteiro['Faturamento']
dados2 = roteiro['Depósito']['Rev']
dados3 = roteiro['Estoque']
dados4 = roteiro['mercado']
for produto in dados3:
    infoprod = dados3[f'{produto}']
    ean = infoprod['EAN']
    comparacao = (produto,ean)
    if comparacao in lista_ean:
        pass
    else:
       lista_ean.append(comparacao)
with col7:
     selecao_datas=st.date_input(label='selecione uma data',value=None)
     ano = str(selecao_datas)[0:4]
     mes = str(selecao_datas)[5:7]
     dia = str(selecao_datas)[8:] 
    
     selecao_datas= f'{dia}-{mes}-{ano}'              
     if selecao_datas:  
       
      for a in dados:
                  if a == selecao_datas:
                            infos = dados[f'{a}']
                            for processo in infos:
                              if processo in lista_processos:
                                pass
                              else:
                                lista_processos.append(processo)
with col8:   
      if selecao_datas:
        selecao_processos = st.selectbox(label='',placeholder='Selecione um Processo',index=None,options=lista_processos) 
if selecao_datas and selecao_processos:
          for x in dados:
                  if x == selecao_datas:
                          infos = dados[f'{x}']
                          for processo in infos:
                            if processo ==  selecao_processos:
                              notas = infos[f'{processo}']
                              for espec in notas:
                                if espec != 'status' and espec !='separacao':
                                  try:
                                    numero_nota = espec['nota']
                                    cliente = espec['cliente']
                                    data = espec['data']
                                    quantidade =espec['quantidade']
                                    descricao = espec['descricao']
                                    produto = espec['produto']
                                    posi = espec['posicao']
                                    transp = espec['transportadora'] 
                                    dicionario = {'numero_nota':numero_nota,'cliente':cliente,'data':data,'quantidade':quantidade,'descrição':descricao,'produtos':produto,'posi':posi,'transp':transp}  
                                    if dicionario in lista_dicionarios:
                                        pass
                                    else:  
                                        lista_dicionarios.append(dicionario)   
                                  except:
                                    try:
                                      numero_nota = notas[f'{espec}']['nota']
                                    except:
                                      numero_nota = espec['nota']
                                    try:
                                      cliente = notas[f'{espec}']['cliente']
                                    except:
                                      cliente = espec['cliente']
                                    try:
                                      data = notas[f'{espec}']['data']
                                    except:
                                      data = espec['data']
                                    try:
                                      quantidade = notas[f'{espec}']['quantidade']
                                    except:
                                      quantidade = espec['quantidade']
                                    try:
                                      descricao = notas[f'{espec}']['descricao']
                                    except:
                                      descricao = espec['descricao']
                                    try:
                                      produto = notas[f'{espec}']['produto']
                                    except:
                                      produto = espec['produto']
                                    try:
                                      posi = notas[f'{espec}']['posicao']
                                    except:
                                      posi = '00-000-00'
                                    try:
                                      transp = notas[f'{espec}']['transportadora']
                                    except:
                                      transp = espec['transportadora']
                                    dicionario = {'numero_nota':numero_nota,'cliente':cliente,'data':data,'quantidade':quantidade,'descrição':descricao,'produtos':produto,'posi':posi,'transp':transp}
                                    if dicionario in lista_dicionarios:
                                        pass
                                    else:  
                                        lista_dicionarios.append(dicionario)  
                                else:
                                  lista_dicionarios.append('já coletadoSS')
                                
if selecao_datas and selecao_processos:       
        i = 0 
        if 'já coletadoSS' in lista_dicionarios:
          st.info('Mercado já concluido')
          st.divider()  
        else:  
         for item in lista_dicionarios:  
           if item['posi'] != '00-000-00':
              mercado_ativo = True
              for data_mercado in dados4:
                if data_mercado == selecao_datas:
                  
                  for numero_nota in dados4[f'{data_mercado}']:
                    if numero_nota == item['numero_nota']:
                      mercado_ativo  = False
    
              if mercado_ativo == True:
                  st.session_state.qtd = 0
                  st.info(f'''Nota:{item['numero_nota']}\n
                    Cliente:{item['cliente']}\n
          Produto:{item['produtos']}\n
          quantidade: {item['quantidade']}\n
          localização: {item['posi']}''') 
                  acao = st.text_input(label='',placeholder=f'Insira o item {item['produtos']}',key=i)
                  i += 1 
                  if str(acao) == str(item['produtos']):
                      volume_mercado = random.randint(0,10000)
                      caminho_mercado = f'{selecao_datas}/{item['numero_nota']}'
                      dict_mercado = {'cliente':item['cliente'],'processo':selecao_processos,'ean_volume':volume_mercado,'itens':item['produtos'],'nota':item['numero_nota'],'posicao':item['posi'],'mercado_concluido':'sim','quantidade':item['quantidade'],'transp':item['transp']}
                      ref_mercado.child(caminho_mercado).set(dict_mercado)
                      st.success(f'Mercado de volume: {volume_mercado} registrado')
                  st.divider() 
