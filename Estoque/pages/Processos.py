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
caminho_faturamento = f'{data_atual}'
ref_faturamento.child(caminho_faturamento).set('a')
