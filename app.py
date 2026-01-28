import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والواجهة
st.set_page_config(page_title="SALEH AI PRO", page_icon="👑", layout="centered")

# ستايل CSS متطور
st.markdown("""
    <style>
    .main { background-color: #050505; }
    .stChatMessage { border-radius: 20px; margin-bottom: 10px; border: 1px solid #333; }
    .stChatMessage[data-testid="stChatMessageUser"] { background-color: #1a1a1a; border-color: #D4AF37; }
    .stChatMessage[data-testid="stChatMessageAssistant"] { background-color: #0d0d0d; border-color: #444; }
    .stChatInputContainer { padding-bottom: 20px; }
    h1 { color: #D4AF37; text-align: center; font-family: 'Cairo', sans-serif; text-shadow: 2px 2px 4px #000; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #D4AF37; color: black; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #b8962e; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("👑 SALEH AI - PRO")

# 2. إعداد الـ API
API_KEY = "AIzaSyA83bkpXNvLB7bmcqOpDi7ucGYqI7K7kD4"
genai.configure(api_key=API_KEY)

# وظيفة البحث عن الموديل
@st.cache_resource
def get_model():
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m in models:
            if 'gemini-1.5-flash' in m: return m
        return models[0]
    except: return 'gemini-1.5-flash'

model = genai.GenerativeModel(get_model())

# 3. إدارة الذاكرة (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# زر مسح المحادثة في القائمة الجانبية
with st.sidebar:
    st.header("الإعدادات")
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.write("إصدار: 2.0 (Gold Edition)")
    st.write("المطور: صالح")

# 4. عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطقة الإدخال والرد
if prompt := st.chat_input("تحدث مع ذكاء صالح..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # رد الذكاء الاصطناعي
    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير..."):
            try:
                # إضافة تعليمات خفية للموديل ليكون مساعد صالح
                full_prompt = f"أنت الآن SALEH AI، مساعد ذكي وشخصي لصالح. رد عليه باحترافية وود. السؤال هو: {prompt}"
                response = model.generate_content(full_prompt)
                
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.error("لم يتم استلام رد.")
            except Exception as e:
                st.error(f"خطأ: {e}")
