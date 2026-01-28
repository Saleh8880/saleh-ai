import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SALEH AI PRO", page_icon="👑")

# ستايل ذهبي
st.markdown("<style>.main { background-color: #050505; } div[data-testid='stChatMessage'] { border-radius: 15px; border: 1px solid #D4AF37; }</style>", unsafe_allow_html=True)

st.title("👑 SALEH AI - GOLD")

# المفتاح الخاص بك
API_KEY = "AIzaSyA83bkpXNvLB7bmcqOpDi7ucGYqI7K7kD4"
genai.configure(api_key=API_KEY)

# دالة ذكية لاختيار الموديل المتاح فعلياً لحسابك
@st.cache_resource
def load_working_model():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # محاولة ترتيب الأولويات: فلاش أولاً ثم برو
    for target in ['models/gemini-1.5-flash', 'models/gemini-1.0-pro', 'models/gemini-pro']:
        if target in available_models:
            return genai.GenerativeModel(target)
    return genai.GenerativeModel(available_models[0])

try:
    model = load_working_model()
except:
    st.error("عذراً صالح، هناك مشكلة في الربط مع جوجل حالياً.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسأل صالح AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # إضافة نظام محاولة إعادة الإرسال في حال الخطأ
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            if "429" in str(e):
                st.warning("⚠️ جوجل تعبانة شوية من كتر الأسئلة! استنى 30 ثانية وابعث تاني.")
            else:
                st.error(f"حدث خطأ: {e}")
