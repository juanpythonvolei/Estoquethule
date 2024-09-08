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
#caminho_faturamento = f'{data_atual}'
#ref_faturamento.child(caminho_faturamento).set('a')
dados = roteiro['Faturamento']
dados2 = roteiro['Depósito']['Rev'] 
dados4 = roteiro['mercado']
dados5 = roteiro['separacao']
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
                                  posi = espec['posicao']
                                  transp = espec['transportadora'] 
                                  dicionario = {'numero_nota':numero_nota,'cliente':cliente,'data':data,'quantidade':quantidade,'descrição':descricao,'produtos':produto,'posi':posi,'transp':transp}  
                                  if dicionario in lista_dicionarios:
                                      pass
                                  else:  
                                      lista_dicionarios.append(dicionario)   
                                except:
                                  numero_nota = notas[f'{espec}']['nota']
                                  cliente = notas[f'{espec}']['cliente']
                                  data = notas[f'{espec}']['data']
                                  quantidade = notas[f'{espec}']['quantidade']
                                  descricao = notas[f'{espec}']['descricao']
                                  produto = notas[f'{espec}']['produto']
                                  posi = notas[f'{espec}']['posicao']
                                  transp = notas[f'{espec}']['transportadora']
                                  dicionario = {'numero_nota':numero_nota,'cliente':cliente,'data':data,'quantidade':quantidade,'descrição':descricao,'produtos':produto,'posi':posi,'transp':transp}
                                  if dicionario in lista_dicionarios:
                                      pass
                                  else:  
                                      lista_dicionarios.append(dicionario)  
                              else:
                                lista_dicionarios.append('já coletadoSS')
                              
  if selecao_datas and selecao_processos:       
    i = 0 
    try: 
      if 'já coletadoSS' in lista_dicionarios:
        st.info('Mercado já concluido')
        st.divider()  
      else:
       for item in lista_dicionarios:  
            st.info(f'''Nota:{item['numero_nota']}\n
                  Cliente:{item['cliente']}\n
        Produto:{item['produtos']}\n
        quantidade: {item['quantidade']}\n
        localização: {item['posi']}''') 
            acao = st.text_input(label='',placeholder=f'Insira o item {item['produtos']}',key=i)
            i += 1 
            if str(acao) == str(item['produtos']):
                volume_mercado = random.randint(0,10000)
                caminho_mercado = f'{selecao_datas}/{volume_mercado}'
                dict_mercado = {'cliente':item['cliente'],'processo':selecao_processos,'ean_volume':volume_mercado,'itens':item['produtos'],'nota':item['numero_nota'],'posicao':item['posi'],'mercado_concluido':'sim','quantidade':item['quantidade'],'transp':item['transp']}
                ref_mercado.child(caminho_mercado).set(dict_mercado)
                st.success(f'Mercado de volume: {volume_mercado} registrado')
            st.divider() 
    except:
        pass 

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
    
    for y in dados4:
                  
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
        
       for dict in lista_separacao:
         separacao_ativa = False
         for m in dados5:
           if m == selecao_datas_separacao:
             tranpostador_m = dados5[f'{m}']
             for nota_m in tranpostador_m:
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
              ver_comparar = (dict['produtos'],dict['posi'],dict['quantidade'],dict['cliente'],dict['ean_volume'])
              st.title(f'Nota: {dict['numero_nota']}') 
              col4,col5,col6 = st.columns(3)
              with col4:
                ean_valido_produto = st.text_input(label = f'código ean do produto:  {dict['produtos']}',key=i)
                i += 1
                if ean_valido_produto==ver_comparar[0]:
                    st.info(f'{dict['produtos']} ok')
                else:
                  ean_valido_produto = None
              with col5:
                      ean_valido_volume = st.text_input(label = f'código ean do volume {dict['ean_volume']}' ,key=i)
                      i += 1 
                      if str(ean_valido_volume) == str(ver_comparar[4]):
                        st.info('Volume ok')
                      else:
                        ean_valido_volume = None
              with col6:
                            ean_valido_posicao = st.text_input(label = f'código ean da posição: {dict['posi']}',key=i)
                            i += 1
                            if ean_valido_posicao == ver_comparar[1]:
                              st.info(f'Posição {dict['posi']} ok')
                              st.info(f'Nota {dict['numero_nota']} separada com sucesso')
                            else:
                              ean_valido_posicao = None
              if ean_valido_produto and ean_valido_volume and ean_valido_posicao:
                selecao_datas_separacao2 = f'{dia}-{mes}-{ano}' 
                caminho_separacao = f'{selecao_datas_separacao2}/{dict['transportadora'][:5]}/{dict['numero_nota']}'
                dict_separacao = {
                    'cliente':dict['cliente'],
                    'nota':dict['numero_nota'],
                    'volumes':dict['quantidade'],
                    'separacao_concluido':'sim'
                }
                ref_separacao.child(caminho_separacao).set(dict_separacao)
                st.success(f'Separacao da nota {dict['numero_nota']} concluida com sucesso')
               
           st.divider()
             
    
     
                   
                
        

