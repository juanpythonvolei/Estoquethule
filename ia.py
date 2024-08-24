GOOGLE_API_KEY = st.secrets['firebase']['GOOGLE_API_KEY']
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])
