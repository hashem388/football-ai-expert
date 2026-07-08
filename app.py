import streamlit as st
import google.generativeai as genai
from serpapi import GoogleSearch

st.set_page_config(page_title="Football AI Expert", layout="wide")

# تصميم عصري (CSS احترافي)
st.markdown("""
    <style>
    .card {background: #1e1e1e; padding: 30px; border-radius: 20px; text-align: center; cursor: pointer; border: 1px solid #333; transition: 0.3s;}
    .card:hover {background: #2a2a2a; transform: translateY(-5px);}
    .stChatInput {position: fixed; bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# مفاتيح الأمان
with st.sidebar:
    api_gemini = st.text_input("Gemini API Key", type="password")
    api_serp = st.text_input("SerpApi Key", type="password")

if not api_gemini or not api_serp:
    st.info("أدخل المفاتيح في القائمة الجانبية للبدء.")
    st.stop()

genai.configure(api_key=api_gemini)
model = genai.GenerativeModel('gemini-1.5-flash')

# تعريف الصفحات (Routing)
if 'page' not in st.session_state: st.session_state.page = 'home'

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.title("⚽ Football AI Expert")
    items = [
        {"name": "الدوري الإنجليزي", "icon": "🏴󠁧󠁢󠁥󠁮󠁧󠁿"}, {"name": "الدوري الإسباني", "icon": "🇪🇸"},
        {"name": "خبير الفانتازي", "icon": "🏆"}, {"name": "مقارنة لاعبين", "icon": "⚔️"}
    ]
    cols = st.columns(2)
    for i, item in enumerate(items):
        with cols[i%2]:
            if st.button(f"{item['icon']} {item['name']}", key=item['name']):
                st.session_state.page = item['name']
                st.rerun()

# --- صفحة الشات (مشتركة لكل الأقسام) ---
else:
    if st.button("⬅️ العودة للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.subheader(f"مرحباً بك في شات {st.session_state.page}")
    
    # اقتراحات ذكية فوق الشات
    suggestions = ["أهم أخبار اليوم؟", "تحليل أداء الفريق؟", "توقعات المباراة القادمة؟"]
    cols_sug = st.columns(3)
    for i, sug in enumerate(suggestions):
        if cols_sug[i].button(sug): st.session_state.q = sug

    # محرك الشات
    user_q = st.chat_input("اكتب سؤالك هنا...")
    if "q" in st.session_state:
        user_q = st.session_state.q
        del st.session_state.q

    if user_q:
        with st.chat_message("user"): st.markdown(user_q)
        with st.chat_message("assistant"):
            with st.spinner("جاري التحليل..."):
                search = GoogleSearch({"q": f"{st.session_state.page} {user_q}", "api_key": api_serp})
                res = model.generate_content(f"أنت محلل كرة قدم خبير في {st.session_state.page}. أجب: {user_q}").text
                st.markdown(res)
