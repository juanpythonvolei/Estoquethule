
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
  pass

#ref_separacao = db.reference('separacao')
#caminho_separacao = f'algo'
#ref_separacao.child(caminho_separacao).set('a')
ref_separacao = db.reference('separacao')
col1,col2,col3 = st.columns(3)
lista_separacao = []
lista_transp = []
selecao_datas_separacao=st.date_input(label='selecione uma data',key='separacao',value = data_hora_atual)
ano = str(selecao_datas_separacao)[0:4]
mes = str(selecao_datas_separacao)[5:7]
dia = str(selecao_datas_separacao)[8:] 
selecao_datas_separacao = f'{dia}-{mes}-{ano}' 

if selecao_datas_separacao:
    if dados4 == None:
      pass
    else:
      for y in dados4:
                    if y == selecao_datas_separacao:
                            infos = dados4[f'{y}']
                            for nota in infos:
                                elementos = infos[f'{nota}']
                                
                                if elementos['mercado_concluido'] == 'sim':
                                        numero_nota = elementos['nota']
                                        cliente =elementos['cliente']
                                        quantidade = elementos['quantidade']
                                        #descricao =elemento['descricao']
                                        produto = elementos['itens']
                                        posi =elementos['posicao']
                                        transportadora =elementos['transp']
                                        ean_volume = elementos['ean_volume']
                                        
                                        dicionario = {'ean_volume':ean_volume,'numero_nota':numero_nota,'cliente':cliente,'quantidade':quantidade,'produtos':produto,'posi':posi,'transportadora':transportadora,"ean_volume":ean_volume}  
                                        if dicionario in lista_separacao:
                                          pass
                                        else:
                                          lista_separacao.append(dicionario)
      i = 0                            
      for dict in lista_separacao:
       
       transp = dict['transportadora']
       transp = str(transp).casefold()
       if 'ltda.' in transp:
         transp = transp.replace('ltda.','ltda')
       if transp in lista_transp:
         pass
       else:
         lista_transp.append(transp)
      selecao_transp = st.selectbox(label='',placeholder='Selecione uma tranportadora',options=lista_transp,index=None)
  
      
      if selecao_transp:
        selecao_transp = selecao_transp[:5].upper()
        for dict in lista_separacao:
           separacao_ativa = False 
           for m in dados5:
             if m == selecao_datas_separacao:
               tranpostador_m = dados5[f'{m}']
               st.write(tranpostador_m)
               for nota_m in tranpostador_m:
                 st.write(selecao_transp)
                 st.write(nota_m)
                 if selecao_transp == str(nota_m):
                   caracs = tranpostador_m[f'{nota_m}']
                   for carac in caracs:
                       numero_nota_m = caracs[f'{carac}']['nota']
                       if numero_nota_m == dict['numero_nota']:
                         if caracs[f'{carac}']['separacao_concluido'] == 'sim':
                          separacao_ativa = True
           if separacao_ativa == False: 
             lista_tuplas_separacao = [] 
             transp_dict = str(dict['transportadora']).casefold()
             if 'ltda.' in transp_dict:
               transp_dict = transp_dict.replace('ltda.','ltda')
             if transp_dict == selecao_transp:
                st.title(f'Nota: {dict['numero_nota']}') 
                col4,col5,col6 = st.columns(3)
                with col4:
                  ean_valido_produto = st.text_input(label = f'código ean do produto:  {dict['produtos']}',key=i)
                  if ean_valido_produto or not ean_valido_produto:
                    i += 1
                  if str(ean_valido_produto) == str(dict['produtos']):
                      st.info(f'{dict['produtos']} ok')
                  else:
                    ean_valido_produto = None
                with col5:
                        ean_valido_volume = st.text_input(label = f'código ean do volume {dict['ean_volume']}' ,key=i)
                        if ean_valido_volume or not ean_valido_volume:
                          i += 1 
                        if str(ean_valido_volume) == str(dict['ean_volume']):
                          st.info('Volume ok')
                        else:
                          ean_valido_volume = None
                with col6:
                              ean_valido_posicao = st.text_input(label = f'código ean da posição: {dict['posi']}',key=i)
                              if ean_valido_posicao or not ean_valido_posicao:
                                i += 1
                              if ean_valido_posicao == dict['posi']:
                                st.info(f'Posição {dict['posi']} ok')
                                st.info(f'Nota {dict['numero_nota']} separada com sucesso')
                              else:
                                ean_valido_posicao = None
                if ean_valido_produto and ean_valido_volume and ean_valido_posicao:
                  selecao_datas_separacao2 = f'{dia}-{mes}-{ano}' 
                  caminho_separacao = f'{selecao_datas_separacao2}/{str(dict['transportadora'][:5]).upper()}/{dict['numero_nota']}'
                  dict_separacao = {
                      'cliente':dict['cliente'],
                      'nota':dict['numero_nota'],
                      'volumes':dict['quantidade'],
                      'separacao_concluido':'sim'
                  }
                  ref_separacao.child(caminho_separacao).set(dict_separacao)
                  st.success(f'Separacao da nota {dict['numero_nota']} concluida com sucesso')
                 
             st.divider()
