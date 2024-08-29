import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore,db
import requests
import os
import requests
requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
roteiro = requiscao.json()
if 'Estoque' in roteiro:
    dados = roteiro['Estoque']
    
    lista_nomes_verif = [item for item in dados]
    image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
    codigo = st.text_input(label='',placeholder='Insira o Código do produto')
    if codigo not in lista_nomes_verif:
        descricao = st.text_input(label='',placeholder='Insira uma descirção do produto')
        col1,col2,col3 = st.columns(3)
        with col1:
            foto = st.text_input(label='',placeholder='Insira a foto do Produto')
        with col2:
            with st.popover('📷'):
             uploaded_files = st.file_uploader("Escolha a foto", type=['png','jpg'], accept_multiple_files=False)
        col1,col2,col3 = st.columns(3)
        
        
        @st.dialog(f"Deseja realmente excluir o produtos") 
        def exclusao():
            try:
                requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
                roteiro = requiscao.json()
                dados = roteiro['Estoque']
                dados2 = roteiro['Depósito']['Rev']
                lista_nomes = [item for item in dados]
                lista_nomes_rec = [item for item in dados]
                produto_excluir = st.selectbox(label='',options=lista_nomes,index=None,placeholder='Selecione um produto')       
                if produto_excluir:
                            veiculo_ref = db.reference(f'Estoque/{produto_excluir}')
                            rec_ref = db.reference(f'Depósito/Rec/{produto_excluir}')
                            veiculo_ref.delete()
                            rec_ref.delete()
                            for item in dados2:
                                st.write(item)
                                produto = dados2[f'{item}']
                                
                                rev_ref = db.reference(f'Depósito/Rev/{item}/{produto_excluir}')
                                rev_ref.delete()
                            st.success(f'Produto {produto_excluir} excluido')
                else:
                        st.info(f'Você realmente deseja excluir o produto {produto_excluir}')
            except:
                st.info('Por enquanto, não foram registrados produtos')
        
        
        excluir = st.button('Excluir Produtos',key='botao_excluir')
        if excluir:
                exclusao()
        with st.popover('Alterar informações de Produtos'):
            
            requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
            roteiro = requiscao.json()
            dados = roteiro['Estoque']
            lista_produto_alteracao = []
            lista_alteracao_campo = []
            for item in dados:
                lista_produto_alteracao.append(item)
                for elemento in dados[f'{item}']:
                    if elemento in lista_alteracao_campo:
                        pass
                    else:
                        lista_alteracao_campo.append(elemento)
            alteracao_item = st.selectbox(placeholder='Selecione a alteração',label='',options=lista_produto_alteracao,index=None)
            if alteracao_item:
                   alteracao_campo = st.selectbox(placeholder='Selecione a alteração',label='',options=lista_alteracao_campo,index=None) 
                   if alteracao_campo: 
                        item_alterado = st.text_input(placeholder='Insira a substituição',label='')
                        if item_alterado:
                            caminho_final = f'{alteracao_item}/{alteracao_campo}'
                            deposito_ref.child(caminho_final).set(item_alterado)
                            st.success(f'O item {alteracao_item} foi alterado no campo {alteracao_campo} para o valor de {item_alterado}')
        if codigo and descricao and foto or uploaded_files:
            ref = db.reference('Estoque')
            with col1:
                cadastro = st.button('Cadastar Produtos')
                if cadastro:
                    if foto:
                        
                        dict_produto = {'Foto':foto,'Descrição':descricao}
                        caminho_cadastro = f'{codigo}'
                        ref.child(caminho_cadastro).set({
                                    'foto':foto,
                                    'Descrição':descricao
                                })
                    elif uploaded_files:
                                    caminho_cadastro = f'{codigo}'
                                    ref.child(caminho_cadastro).set({
                                    'foto':f'{uploaded_files.name}',
                                    'Descrição':descricao
                                })
    
            
        else:
                st.error('Ainda há campos a serem preenchidos')
    else:
        st.error(f'O item {codigo} já existe no cadastro')
else:
    image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
    codigo = st.text_input(label='',placeholder='Insira o Código do produto',key='codigo')
    descricao = st.text_input(label='',placeholder='Insira uma descirção do produto',key='descricao')
    col1,col2,col3 = st.columns(3)
    with col1:
            foto = st.text_input(label='',placeholder='Insira a foto do Produto',key='foto')
    with col2:
            with st.popover('📷'):
             uploaded_files = st.file_uploader("Escolha a foto", type=['png','jpg'], accept_multiple_files=False,key='upload')
    col1,col2,col3 = st.columns(3)
    if codigo and descricao and foto or uploaded_files:
            
            with col1:
                cadastro = st.button('Cadastar Produtos',key='cadastro')
                if cadastro:
                    if foto:
                        dict_produto = {'Foto':foto,'Descrição':descricao}
                    
                        caminho_cadastro = f'Estoque/{codigo}'
                        ref.child(caminho_cadastro).set(dict_prpduto)
                        
