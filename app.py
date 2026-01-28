import streamlit as st
import requests

# --- 1. إعدادات الصفحة ---
st.set_page_config(
    page_title="SALEH AI PRO",
    page_icon="👑",
    layout="centered"
)

# --- 2. التصميم الاحترافي (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }
    .stApp {
        background-color: #0e1117;
    }
    h1 {
        color: #FFD700 !important;
        text-align: center;
        border-bottom: 1px solid #333;
        padding-bottom: 20px;
    }
    .stChatMessage {
        background-color: #262730;
        border-radius: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. المتغيرات ---
NEW_API_KEY = "AIzaSyAap0wkUBLjvHgmKe4sfil8FWgoc3Tfp5M"

# --- 4. دالة اختيار الموديل (تم التعديل للإصلاح) ---
def find_any_working_model():
    # ⚠️ التعديل هنا: بدلاً من البحث العشوائي الذي يسبب مشاكل 403
    # سنقوم بإرجاع الموديل المستقر والمجاني مباشرة
    return "models/gemini-1.5-flash"

# --- 5. واجهة التطبيق ---
with st.sidebar:
    st.title("⚙️ لوحة التحكم")
    st.write("حالة النظام: **متصل** ✅")
    st.caption("الموديل المستخدم: Gemini 1.5 Flash")
    if st.button("مسح المحادثة 🗑️"):
        st.session_state.messages = []
        st.rerun()

st.title("👑 SALEH AI - ULTIMATE")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    avatar = "👑" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- 6. المعالجة ---
if prompt := st.chat_input("اسأل صالح AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="👑"):
        status_placeholder = st.empty()
        status_placeholder.markdown("⏳ *جاري الاتصال...*")
        
        # استدعاء الدالة (التي سترجع الآن الموديل الصحيح فقط)
        working_model = find_any_working_model()
        
        url = f"https://generativelanguage.googleapis.com/v1beta/{working_model}:generateContent?key={NEW_API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            res = requests.post(url, json=payload)
            
            if res.status_code == 200:
                data = res.json()
                ans = data['candidates'][0]['content']['parts'][0]['text']
                status_placeholder.empty()
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            else:
                status_placeholder.empty()
                # طباعة تفاصيل الخطأ للمساعدة في التشخيص
                st.error(f"⚠️ خطأ ({res.status_code}): الموديل {working_model} لم يستجب.")
                st.code(res.text) # سيعرض لنا رسالة جوجل بالضبط لو حدث خطأ
                
        except Exception as e:
            status_placeholder.empty()
            st.error(f"حدث خطأ برمجي: {e}")
