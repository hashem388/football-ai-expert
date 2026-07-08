import streamlit as st
import google.generativeai as genai
from google_search_results import GoogleSearch # تأكد من تثبيت هذه المكتبة

# إعداد الصفحة
st.set_page_config(page_title="Football AI Expert", layout="wide")

# تصميم الألوان الفخم (CSS)
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {gap: 20px;}
    .stTabs [data-baseweb="tab"] {height: 50px; background-color: #1a1a1a; color: white; border-radius: 10px;}
    .stApp {background-color: #0e1117;}
    </style>
""", unsafe_allow_html=True)

# إدارة المفاتيح (مخفية في الـ Sidebar)
with st.sidebar:
    api_gemini = st.text_input("Gemini API Key", type="password")
    api_serp = st.text_input("SerpApi Key", type="password")

if not api_gemini or not api_serp:
    st.warning("يرجى إدخال مفاتيح الـ API في القائمة الجانبية.")
    st.stop()

genai.configure(api_key=api_gemini)
model = genai.GenerativeModel('gemini-1.5-flash')

# الأقسام
tab1, tab2, tab3 = st.tabs(["⚽ الرئيسية (نتائج حية)", "🇪🇸 الدوري الإسباني", "🏆 خبير الفانتازي"])

# --- التبويب الأول: الرئيسية ---
with tab1:
    st.header("النتائج الحية والأخبار العاجلة")
    # هنا يتم الربط مع API-Football في المستقبل
    st.info("جارٍ جلب البيانات اللحظية...")

# --- التبويب الثاني: الدوريات (مثال للإسباني) ---
with tab2:
    st.header("تحليل الدوري الإسباني")
    prompt = st.text_input("عن ماذا تريد أن تسأل في الليغا؟")
    if prompt:
        with st.spinner("الخبير يحلل..."):
            # محرك بحث متخصص
            search = GoogleSearch({"q": f"latest La Liga news {prompt}", "api_key": api_serp})
            context = str(search.get_dict().get("organic_results", []))
            res = model.generate_content(f"أنت خبير دوري إسباني. أجب: {prompt} بناءً على: {context}").text
            st.markdown(res)

# --- التبويب الثالث: خبير الفانتازي ---
with tab3:
    st.header("خبير الفانتازي الذكي")
    if st.button("تحليل أفضل لاعبي الجولة الأخيرة"):
        with st.spinner("تحليل أداء اللاعبين والعوامل المؤثرة..."):
            search = GoogleSearch({"q": "Fantasy Premier League best performers last gameweek analysis", "api_key": api_serp})
            context = str(search.get_dict().get("organic_results", []))
            res = model.generate_content(f"أنت خبير فانتازي. حلل لماذا تألق هؤلاء اللاعبون (الأهداف، التمريرات، الفرص). العوامل: {context}").text
            st.markdown(res)
