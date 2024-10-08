import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
import requests           

image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requiscao.json()
if 'Depósito' in roteiro:

  dados = roteiro['Depósito']
  try:
    dados2 = roteiro['Estoque']
  except:
    pass
  
  def consulta(item):    
    if produto in elementos:
      requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
      roteiro = requiscao.json()
      dados = roteiro['Depósito']
      if 'Rev' in dados:
        quantidade_transferida = 0
        dados2 = roteiro['Estoque']
        qtd_Rec = dados['Rec'][f'{item}']['quantidade']
        foto = dados2[f'{item}']['Foto']
        st.warning(f'Item {item} possúi {qtd_Rec} unidades em Rec')
        for elemento in dados['Rev']:
          texto = ''
          localizacao = dados['Rev'][f'{elemento}']
          for x in localizacao:
            if x == item:
                qtd_rev = localizacao[f'{x}']['quantidade']
                if qtd_rev>0:
                  quantidade_transferida += qtd_rev
                  local = localizacao
                  info = f'Item :{item} possúi {qtd_rev} unidades na posição {elemento}' 
                  texto  += info
                  st.info(texto)
        
        try:
          st.image(foto)  
        except:
          pass
        st.metric(label=f'Total transferido',value=quantidade_transferida)
            
  
  
  coletor = st.toggle('Coletor',key='trasferência') 
  col4,col5,col6 = st.columns(3)
  col1,col2,col3 = st.columns(3)
  with col4:
      elementos = [x for x in dados2]
      if coletor:
        produto = st.text_input(label='',placeholder='Insira o produto')
        codigos =  roteiro['Estoque']
        for codigo in codigos:
            item = codigos[f'{codigo}']
            try:
              codigo_ean = item['EAN']
              if codigo_ean == produto:
                produto = codigo
                st.info(f'Você selecionou o item {produto}')
            except:
              produto = produto
              pass
      else:
          produto = st.selectbox(label='',placeholder='Insira o produto',options=elementos,index=None)
  if produto in elementos:
        with col1:
              deposito_origem = st.selectbox(index=None,label='',placeholder='Depósito de origem',options=['Rev','Dev','Rec','Ele'])
        with col2:
              deposito_final= st.selectbox(index=None,label='',placeholder='Depósito final',options=['Rev','Ele'])
        if deposito_origem and deposito_final:
          if produto in elementos:
                deposito_ref = db.reference('Depósito')
                requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
                roteiro = requiscao.json()
                a = roteiro['Depósito']
                if 'Rev' not in a:
                  pass
                else:
                  dados = roteiro['Depósito']['Rev']
                  lista_pos = []
                  for item in dados:
                    posicao = dados[f'{item}']
                    for elemento in posicao:
                                    if elemento == produto:
                                      if item in lista_pos:
                                        pass
                                      else:
                                        lista_pos.append(item)
                  if coletor:
                    if deposito_origem == 'Rec' or deposito_origem == 'Dev'or deposito_origem == 'Ele':
                      origem = st.text_input(label='',placeholder='Insira a posição de Origem',value=deposito_origem)
                    else:
                      origem = st.text_input(label='',placeholder='Insira a posição de Origem')
                      if '#' in origem:
                        origem = origem.replace('#','')
                      if origem:
                        if origem != 'Rec':
                          colum2=origem [3:6]
                          Prat2=origem [0:2]
                          alt2 = origem [7:]
                          if len(colum2) != 3 or len(alt2)!= 2 or len(Prat2)!=2:
                              st.error(f'A posição {origem} está incorreta. Insira-a novamente')
                              origem = None
                          elif int(colum.replace('0','')) > 19 or int(alt.replace('0','')) > 4 or int(Prat.replace('0','')) > 7:
                              st.error(f'A posição {final} não existe')
                              origem = None
                  else:
                    if deposito_origem == 'Rec' or deposito_origem == 'Dev'or deposito_origem == 'Ele':
                      origem = st.text_input(label='',placeholder='Insira a posição de Origem',value=deposito_origem)
                    else:
                      origem = st.selectbox(label='',placeholder='Insira a posição de Origem',options=lista_pos,index=None)     
          
          quantidade = st.number_input(label='',placeholder='Insira a quantidade',value=None)
          if quantidade:
            if deposito_origem == 'Rev':
              quantidade_rev  = roteiro['Depósito'][f'Rev'][f'{origem}'][f'{produto}']['quantidade']
              if quantidade > quantidade_rev:
                quantidade = None
                st.error(f'Atenção, você está inserindo um valor que não pode ser comtemplado na localização {origem} para o produto {produto}')
              else:
                pass
            elif deposito_origem == 'Rec':
                  quantidade_rec = roteiro['Depósito'][f'Rec'][f'{produto}']['quantidade'] 
                  if quantidade > quantidade_rec:
                    quantidade = None
                    st.error(f'Atenção, você está inserindo um valor que não pode ser comtemplado na localização Rec para o produto {produto}')
                  else:
                    pass
          final = st.text_input(label='',placeholder='Insira a posição Final')  
          if final:
                      if '#' in final:
                        final = final.replace('#','')
                      colum=final[3:6]
                      Prat=final[0:2]
                      alt = final[7:]
                      if len(colum) != 3 or len(alt)!= 2 or len(Prat)!=2:
                            st.error(f'A posição {final} está incorreta. Insira-a novamente')
                            final = None
                      elif int(colum.replace('0','')) > 19 or int(alt.replace('0','')) > 4 or int(Prat.replace('0','')) > 7:
                        st.error(f'A posição {final} não existe')
                        final = None
                  
          if origem and produto and quantidade and final:
                      botao_transferir = st.button(f'Transferir {produto}')
                      if botao_transferir:
                          if deposito_origem == 'Rec':
                            requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
                            roteiro = requiscao.json()
                            dados = roteiro['Depósito']
                            quantidade_atual_rec = dados['Rec'][f'{produto}']['quantidade']
                            deposito_ref = db.reference('Depósito')
                            caminho_rec = f'Rec/{produto}/quantidade'
                            nova_quantidade = quantidade_atual_rec-quantidade
                            deposito_ref.child(caminho_rec).set(nova_quantidade)
                            try: 
                              quantidade_atual_rev = dados['Rev'][f'{final}'][f'{produto}']['quantidade']
                              nova_quantidade_rev = quantidade_atual_rev + quantidade
                              caminho_rev = f'Rev/{final}/{produto}'
                              deposito_ref.child(caminho_rev).set({
                              'quantidade':nova_quantidade_rev  # Exemplo de dado adicional
                          })
                              st.success(f'item {produto} transferido para a localização {final}')
                            except:
                              caminho_rev = f'Rev/{final}/{produto}'
                              deposito_ref.child(caminho_rev).set({
                              'quantidade':quantidade  # Exemplo de dado adicional
                          })
                              st.success(f'item {produto} transferido para a localização {final}')
                          elif deposito_origem == 'Rev':
                            requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
                            roteiro = requiscao.json()
                            dados = roteiro['Depósito']
                            quantidade_atual_rev_origem = dados['Rev'][f'{origem}'][f'{produto}']['quantidade']
                            nova_quantidade_rev_origem =  quantidade_atual_rev_origem-quantidade
                            deposito_ref = db.reference('Depósito')
                            caminho_rev_origem = f'Rev/{origem}/{produto}/quantidade'
                            deposito_ref.child(caminho_rev_origem).set(nova_quantidade_rev_origem)
                            try:
                              quantidade_atual_rev_final = dados['Rev'][f'{final}'][f'{produto}']['quantidade']
                            except:
                              quantidade_atual_rev_final = 0
                            nova_quantidade_rev_final =  quantidade_atual_rev_final+quantidade
                            caminho_rev_final = f'Rev/{final}/{produto}/quantidade'
                            deposito_ref.child(caminho_rev_final).set(nova_quantidade_rev_final)
                            st.success(f'Produto {produto} transferido com sucesso')
                            
          else:
                        st.error('Ainda há campos a serem preenchidos')
    
        with col5: 
                  with st.popover('🔍'):
                                 consulta(produto)
        with col6:
                  with st.popover('⚙️'):
                                        deposito_ref = db.reference('Depósito')
                                        requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
                                        roteiro = requiscao.json()
                                        a = roteiro['Depósito']
                                        if 'Rev' not in a:
                                          st.error('Ainda não há rev')
                                        else:
                                          dados = roteiro['Depósito']['Rev']
                                          dados2 = roteiro['Depósito']['Rec']
                                          lista_position = []
                                          for item in dados:
                                            posicao = dados[f'{item}']
                                            for elemento in posicao:
                                              if elemento == produto:
                                                
                                                if item in lista_position:
                                                  pass
                                                else:
                                                  lista_position.append(item)
                                          if coletor:
                                            position = st.text_input(label='',placeholder='Selecione a posição para alteração')
                                          else:
                                            position = st.selectbox(placeholder='Selecione a posição para alteração',index=None,options=lista_position,label='')
                                          if position:
                                            quantidade_rev = dados[f'{position}'][f'{produto}']['quantidade']
                                            qtd = st.number_input(value=None,placeholder='Quantidade para alteração',label='',key='Alteração')
                                            if qtd:
                                              analise = qtd-quantidade_rev
                                              caminho_rev_final = f'Rev/{position}/{produto}/quantidade'
                                              caminho_rec_final = f'Rec/{produto}/quantidade'
                                              deposito_ref.child(caminho_rev_final).set(qtd)
                                              quantidade_rec = roteiro['Depósito']['Rec'][f'{produto}']['quantidade']
                                              if analise >0:
                                                qtd_ofc = quantidade_rec - analise
                                                deposito_ref.child(caminho_rec_final).set(qtd_ofc)
                                              else:
                                                qtd_ofc = quantidade_rec + (analise*-1)
                                                deposito_ref.child(caminho_rec_final).set(qtd_ofc)
                                              st.info(f'Item {produto} teve sua quantidade alterada para {qtd} na posição {position}')   
else:
  st.error('Não há Estoque disponível')
      
                
        
        
