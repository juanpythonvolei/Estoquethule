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
data_hora_atual = datetime.now()
data_atual = data_hora_atual.strftime("%d-%m-%Y")
#caminho_faturamento = f'{data_atual}'
#ref_faturamento.child(caminho_faturamento).set('a')
dados = roteiro['Faturamento']
dados2 = roteiro['Depósito']['Rev'] 
tab1,tab2,tab3 = st.tabs(['Faturamento','Mercado','Separação'])


with tab1:
              lista_filtrada = []         
              uploaded_files = st.file_uploader("Escolha os arquivos", type=[f'xml'], accept_multiple_files=True)
              lista = []   
              contagem = 0    
              erro = 0  
              valor = 0
              lista_ver = []
              if uploaded_files:
                        for nota in uploaded_files:
                          try:
                                             
                                              xml_data = nota.read()
                                              documento = xmltodict.parse(xml_data)
                                              codigo_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['cProd']
                                              numero_da_nota = documento['nfeProc']['NFe']['infNFe']['ide']['nNF']
                                              descricao_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['xProd']       
                                              quantidade_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['qCom'] 
                                              valor_produto = documento['nfeProc']['NFe']['infNFe']['det']['prod']['vProd']
                                              cliente = documento['nfeProc']['NFe']['infNFe']['dest']['xNome']
                                              caminho_faturamento = f'{data_atual}/{numero_da_nota}'
                                              data_emit = documento['nfeProc']['NFe']['infNFe']['ide']['dhEmi'][:10]
                                              for posicao in dados2:
                                                itens_posicao = dados2[f'{posicao}']
                                                for item in itens_posicao:
                                                  try:
                                                    if str(item)  == str(codigo_produto):
                                                      lista_ver.append(
                                                        {
                                                         'produto':item,
                                                         'nota':numero_da_nota,
                                                         'descricao': descricao_produto,
                                                         'quantidade': quantidade_produto,
                                                         'cliente':cliente,
                                                         'valor':valor_produto,
                                                         'data':data_emit 
                                                        
                                                      }
                                                                      )
                                                  except:
                                                    pass
                                                
                          except:
                            pass
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
                                  lista_database.append(info)  
                                  pedido.update({'posicao':posicaoo})
                        
                        caminho_faturamento = f'{data_atual}/{random.randint(10,1000)}'
                        ref_faturamento.child(caminho_faturamento).set(lista_ver)
                        contagem +=1
                        st.metric(label='Notas faturadas',value=contagem)
                            
                          
                                  
                                             
                                                                 
         
with tab2: 
  lista_ean = []
  lista_processos = []
  lista_datas =[]
  lista_dicionarios = []  
  requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
  roteiro = requiscao.json()
  dados = roteiro['Faturamento']
  dados2 = roteiro['Depósito']['Rev']
  dados3 = roteiro['Estoque']
  for produto in dados3:
    infoprod = dados3[f'{produto}']
    ean = infoprod['EAN']
    comparacao = (produto,ean)
    if comparacao in lista_ean:
      pass
    else:
     lista_ean.append(comparacao)
  st.write()
  selecao_datas=st.date_input(label='selecione uma data')
  ano = str(selecao_datas)[0:4]
  mes = str(selecao_datas)[5:7]
  dia = str(selecao_datas)[8:] 
  selecao_datas = f'{dia}-{mes}-{ano}'              
  if selecao_datas:  
    for a in dados:
                if a == selecao_datas:
                          infos = dados[f'{a}']
                          for processo in infos:
                            if processo in lista_processos:
                              pass
                            else:
                              lista_processos.append(processo)
  selecao_processos = st.selectbox(label='',placeholder='Selecione um Processo',index=None,options=lista_processos) 
  if selecao_datas and selecao_processos:
        for x in dados:
                if x == selecao_datas:
                        infos = dados[f'{x}']
                        for processo in infos:
                          if processo ==  selecao_processos:
                            notas = infos[f'{processo}']
                            st.write(notas)
                            if 'status' not in notas:
                             for espec in notas:
                                numero_nota = espec['nota']
                                cliente = espec['cliente']
                                data = espec['data']
                                quantidade = espec['quantidade']
                                descricao = espec['descricao']
                                produto = espec['produto']
                                posi = espec['posicao']
                                dicionario = {'numero_nota':numero_nota,'cliente':cliente,'data':data,'quantidade':quantidade,'descrição':descricao,'produtos':produto,'posi':posi}  
                                if dicionario in lista_dicionarios:
                                    pass
                                else:  
                                    lista_dicionarios.append(dicionario)   
                            else:
                              lista_dicionarios.append('concluido')
  lista_conclusao = []
  contagem = 0
  if 'concluido' not in lista_dicionarios:
    for item in lista_dicionarios:  
        
        lista_conferencia = []
        qtd = int(item['quantidade'][0])
        for i in range(int(qtd)):
            lista_conferencia.append(1)
        col4,col5,col6 = st.columns(3)
        with col4:
            st.info(f'''Nota:{item['numero_nota']}\n
            Cliente:{item['cliente']}\n
    Produto:{item['produtos']}\n''')
        with col5:
            try:
                coleta = st.text_input(label=f'''Posição do item {item['produtos']} 
    
                posição:{item['posi']}''',key=f'{item['produtos']}')
              
                if coleta :
                    for ean_ingo in lista_ean:
                      produto,ean = ean_info
                      if ean == coleta:
                        coleta = produto
                        st.info(f'voce seleiconou o item {produto}')
                    if coleta:    
                      if len(lista_conferencia) > 0:
                        lista_conferencia.remove(1)
                      else:
                      contagem +=1
            except:
                st.error('Item não consta em rev')
                
        with col6:
                    st.metric(f'Quantidade restante',value=len(lista_conferencia))
        
        st.divider()   
    if len(lista_conferencia) == contagem:
                caminho_faturamento = f'{selecao_datas}/{selecao_processos}/status'
                ref_faturamento.child(caminho_faturamento).set('concluido')
                st.success('Processo Concluido')  
  else:
   st.error('mercado já concluído')
           
            
                   
                
        

