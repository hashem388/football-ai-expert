import streamlit as st
import google.generativeai as genai
from google_search_results import GoogleSearch

# إعداد الصفحة
st.set_page_config(page_title="Football AI Expert", layout="wide")

# إعداد مفاتيح الـ API
with st.sidebar:
    api_gemini = st.text_input("Gemini API Key", type="password")
    api_serp = st.text_input("SerpApi Key", type="password")

if not api_gemini or not api_serp:
    st.info("يرجى إدخال مفاتيح الـ API في القائمة الجانبية للبدء.")
    st.stop()

genai.configure(api_key=api_gemini)
model = genai.GenerativeModel('gemini-1.5-flash')

# الأقسام
tab1, tab2, tab3 = st.tabs(["⚽ الرئيسية", "🇪🇸 الدوري الإسباني", "🏆 خبير الفانتازي"])

with tab1:
    st.header("النتائج الحية والأخبار")
    st.write("مرحباً بك في واجهة كرة القدم الذكية.")

with tab2:
    st.header("تحليل الدوري الإسباني")
    prompt = st.text_input("عن ماذا تريد أن تسأل في الليغا؟")
    if prompt:
        search = GoogleSearch({"q": f"latest La Liga news {prompt}", "api_key": api_serp})
        results = search.get_dict().get("organic_results", [])
        context = str(results)
        res = model.generate_content(f"أنت خبير دوري إسباني. أجب: {prompt} بناءً على: {context}").text
        st.markdown(res)

with tab3:
    st.header("خبير الفانتازي الذكي")
    if st.button("تحليل أفضل لاعبي الجولة"):
        search = GoogleSearch({"q": "Fantasy Premier League best performers last gameweek", "api_key": api_serp})
        results = search.get_dict().get("organic_results", [])
        res = model.generate_content(f"حلل أداء اللاعبين في الجولة الأخيرة بناءً على: {str(results)}").text
        st.markdown(res)
