import streamlit as st
from streamlit_option_menu import option_menu
import requests
import time
import google.generativeai as genai
import pandas as pd
from Adicionar_Imagens import exibir_imagem


GOOGLE_API_KEY = st.secrets['firebase']['GOOGLE_API_KEY']
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])
