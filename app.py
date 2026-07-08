import streamlit as st
import google.generativeai as genai
from serpapi import GoogleSearch

# إعداد الصفحة وتفعيل التجاوب مع الموبايل
st.set_page_config(page_title="Football AI Expert", layout="wide")

# تصميم احترافي (الوضع المظلم + بطاقات كبار)
st.markdown("""
    <style>
    .card {background-color: #1e1e1e; padding: 20px; border-radius: 15px; border: 1px solid #444; margin: 10px;}
    .stButton>button {width: 100%; border-radius: 10px; height: 50px;}
    </style>
""", unsafe_allow_html=True)

# مفاتيح الأمان
with st.sidebar:
    st.title("⚙️ الإعدادات")
    api_gemini = st.text_input("Gemini API Key", type="password")
    api_serp = st.text_input("SerpApi Key", type="password")

if not api_gemini or not api_serp:
    st.info("يرجى إدخال المفاتيح في القائمة الجانبية.")
    st.stop()

genai.configure(api_key=api_gemini)
model = genai.GenerativeModel('gemini-1.5-flash')

# 1. نظام البطاقات للدوريات
st.title("⚽ المركز الرئيسي لكرة القدم")
cols = st.columns(5)
leagues = ["الدوري الإنجليزي", "الدوري الإسباني", "الدوري الإيطالي", "الدوري الألماني", "الدوري الفرنسي"]

for i, league in enumerate(leagues):
    with cols[i]:
        if st.button(league):
            st.session_state.active_league = league

# 2. منطقة الشات الذكي (تتغير حسب الدوري)
if "active_league" in st.session_state:
    st.subheader(f"شات خاص: {st.session_state.active_league}")
    
    # اقتراحات ذكية للمستخدم
    st.write("اقتراحات:")
    col1, col2, col3 = st.columns(3)
    if col1.button("أهم أخبار الانتقالات؟"): st.session_state.user_q = "أهم أخبار الانتقالات؟"
    if col2.button("تحليل التشكيلة؟"): st.session_state.user_q = "تحليل التشكيلة؟"
    if col3.button("نقاط ضعف الفريق؟"): st.session_state.user_q = "نقاط ضعف الفريق؟"

    # الشات
    user_prompt = st.chat_input("اكتب سؤالك هنا...")
    if "user_q" in st.session_state:
        user_prompt = st.session_state.user_q
        del st.session_state.user_q

    if user_prompt:
        with st.chat_message("assistant"):
            search = GoogleSearch({"q": f"{st.session_state.active_league} {user_prompt}", "api_key": api_serp})
            res = model.generate_content(f"أنت خبير في {st.session_state.active_league}. أجب على: {user_prompt}").text
            st.markdown(res)

# 3. إضافات سريعة (مسابقات ومقارنات)
st.divider()
st.subheader("🛠️ أدوات الخبير")
tool_col1, tool_col2 = st.columns(2)
with tool_col1:
    if st.button("تحدي المسابقات والأسئلة"):
        st.write("هل أنت جاهز؟ (جاري تحديث القاعدة...)")
with tool_col2:
    if st.button("مقارنة لاعبين (Head-to-Head)"):
        st.write("أدخل اسم اللاعبين للمقارنة...")
