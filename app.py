import streamlit as st
import google.generativeai as genai
from serpapi import GoogleSearch

st.set_page_config(page_title="Football AI Expert", page_icon="⚽", layout="wide")

st.title("⚽ خبير كرة القدم العالمي")

# إعداد المفاتيح (أمان عالي: المستخدم يدخلها بنفسه عند فتح الموقع)
api_gemini = st.sidebar.text_input("Gemini API Key", type="password")
api_serp = st.sidebar.text_input("SerpApi Key", type="password")

if api_gemini and api_serp:
    genai.configure(api_key=api_gemini)
    model = genai.GenerativeModel('gemini-1.5-flash')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("اسألني عن أي مباراة أو تحليل..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            search = GoogleSearch({"q": prompt, "api_key": api_serp})
            results = search.get_dict().get("organic_results", [])
            context = str(results)
            
            response = model.generate_content(f"أنت خبير كروي. أجب بدقة بناءً على البيانات: {context}. السؤال: {prompt}").text
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.info("أهلاً بك! يرجى إدخال مفاتيح الـ API في القائمة الجانبية (Sidebar) للبدء.")
