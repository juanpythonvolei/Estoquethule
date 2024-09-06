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
                                  lista_database.append(info)  
                                  pedido.update({'posicao':posicaoo})
                                  contagem +=1
                       
                        caminho_faturamento = f'{data_atual}/{random.randint(10,1000)}'
                        ref_faturamento.child(caminho_faturamento).set(lista_ver)
                        st.metric(label='Notas faturadas',value=contagem)
                        st.metric(label='Produtos não estocados',value=len(list(set(nao_rev))))
                        if len(nao_rev) > 0:
                          st.metric(label='Notas não Faturadas',value=len(list(set(lista_nao))))
                            
                          
                                
                                             
                                                                 
         
with tab2: 
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
  for produto in dados3:
    infoprod = dados3[f'{produto}']
    ean = infoprod['EAN']
    comparacao = (produto,ean)
    if comparacao in lista_ean:
      pass
    else:
     lista_ean.append(comparacao)
  with col7:
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
                                  posi =espec['posicao']
                                  dicionario = {'numero_nota':numero_nota,'cliente':cliente,'data':data,'quantidade':quantidade,'descrição':descricao,'produtos':produto,'posi':posi}  
                                  if dicionario in lista_dicionarios:
                                      pass
                                  else:  
                                      lista_dicionarios.append(dicionario)   
                                except:
                                  numero_nota = notas[f'{espec}']['nota']
                                  cliente = notas[f'{espec}']['cliente']
                                  data = notas[f'{espec}']['data']
                                  quantidade =notas[f'{espec}']['quantidade']
                                  descricao = notas[f'{espec}']['descricao']
                                  produto = notas[f'{espec}']['produto']
                                  posi =notas[f'{espec}']['posicao']
                                  dicionario = {'numero_nota':numero_nota,'cliente':cliente,'data':data,'quantidade':quantidade,'descrição':descricao,'produtos':produto,'posi':posi}
                              else:
                                pass
  if selecao_datas and selecao_processos:                          
   contagem_final = [] 
   for item in lista_dicionarios:  
        quantidade_mercado = int(item['quantidade'])
        contagem = []
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
                    for ean_info in lista_ean:
                      produto,ean = ean_info
                      if ean == coleta:
                        coleta = produto
                        st.info(f'voce seleiconou o item {produto}')
                    if coleta:    
                      if len(contagem) < quantidade_mercado:
                        contagem.append('ok')
                      else:
                        contagem_final.append('ok')
            except:
                st.error('Item não consta em rev')
                
        with col6:
                    st.metric(f'Quantidade restante',value=len(contagem))
        
        st.divider()   
   st.write(len(lista_dicionarios))
   st.write(contagem_final) 
   if contagem_final == len(lista_dicionarios):
                caminho_faturamento = f'{selecao_datas}/{selecao_processos}/status'
                ref_faturamento.child(caminho_faturamento).set('concluido')
                caminho_faturamento = f'{selecao_datas}/{selecao_processos}/separacao'
                ref_faturamento.child(caminho_faturamento).set('aberto')
                st.success('Processo Concluido')  

with tab3:
  ref_separacao = db.reference('separacao')
  
  col1,col2,col3 = st.columns(3)
  lista_separacao = []
  lista_transp = []
  selecao_datas_separacao=st.date_input(label='selecione uma data',key='separacao')
  ano = str(selecao_datas_separacao)[0:4]
  mes = str(selecao_datas_separacao)[5:7]
  dia = str(selecao_datas_separacao)[8:] 
  selecao_datas_separacao = f'{dia}-{mes}-{ano}' 

  if selecao_datas_separacao:
    for y in dados:
                  
                          infos = dados[f'{y}']
                          for processo in infos:
                              notasy = infos[f'{processo}']
                              
                              for espec_sep in notasy:
                                  
                                  if espec_sep != 'status' and espec_sep!='separacao':
                                    try: 
                                      numero_nota = notasy[f'{espec_sep}']['nota']
                                      cliente =notasy[f'{espec_sep}']['cliente']
                                      data = notasy[f'{espec_sep}']['data']
                                      quantidade = notasy[f'{espec_sep}']['quantidade']
                                      descricao =notasy[f'{espec_sep}']['descricao']
                                      produto = notasy[f'{espec_sep}']['produto']
                                      posi =notasy[f'{espec_sep}']['posicao']
                                      transportadora = notasy[f'{espec_sep}']['transportadora']
                                      dicionario = {'numero_nota':numero_nota,'cliente':cliente,'data':data,'quantidade':quantidade,'descrição':descricao,'produtos':produto,'posi':posi,'transportadora':transportadora}  
                                      if dicionario in lista_separacao:
                                        pass
                                      else:
                                        lista_separacao.append(dicionario)
                                    except:
                                      numero_nota = espec_sep['nota']
                                      cliente =espec_sep['cliente']
                                      data = espec_sep['data']
                                      quantidade = espec_sep['quantidade']
                                      descricao =espec_sep['descricao']
                                      produto = espec_sep['produto']
                                      posi =espec_sep['posicao']
                                      transportadora = espec_sep['transportadora']
                                      dicionario = {'numero_nota':numero_nota,'cliente':cliente,'data':data,'quantidade':quantidade,'descrição':descricao,'produtos':produto,'posi':posi,'transportadora':transportadora}  
                                  else:
                                        pass
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
       for dict in lista_separacao:
         transp_dict = str(dict['transportadora']).casefold()
         if 'ltda.' in transp_dict:
           transp_dict = transp_dict.replace('ltda.','ltda')
         if transp_dict == selecao_transp:
            ver_comparar = (dict['produtos'],dict['posi'],dict['quantidade']) 
            st.title(f'Nota: {dict['numero_nota']}') 
            col4,col5,col6 = st.columns(3)
            with col4:
              ean_valido_produto = st.text_input(label = '',placeholder=f'Insira o código ean do produto:  {dict['produtos']}',key=i)
              i += 1
              if ean_valido_produto==ver_comparar[0]:
                  st.info(f'{dict['produtos']} ok')
                  with col5:
                    ean_valido_volume = st.text_input(label = '',placeholder='Insira o código ean do volume',key=i)
                    i += 1 
                    if ean_valido_volume:
                      with col6:
                        ean_valido_posicao = st.text_input(label = '',placeholder=f'Insira o código ean da posição: {dict['posi']}',key=i)
                        i += 1
                        if ean_valid_posicao == ver_comparar[1]:
                          st.info(f'Posição {dict['posi']} ok')
       st.divider()
           
    
     
                   
                
        

