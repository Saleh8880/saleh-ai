import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SALEH AI", page_icon="👑")

# تنسيق الواجهة
st.markdown("<style>.main { background: #000; } div[data-testid='stChatMessage'] { background: #111; border: 1px solid #D4AF37; border-radius: 15px; }</style>", unsafe_allow_html=True)

st.title("👑 SALEH AI - PRO")

# إعداد الـ API
API_KEY = "AIzaSyA83bkpXNvLB7bmcqOpDi7ucGYqI7K7kD4"
genai.configure(api_key=API_KEY)

# وظيفة ذكية لاكتشاف الموديل المتاح لحسابك
@st.cache_resource
def find_my_model():
    try:
        # بنسأل جوجل: إيه اللي شغال عندي بالظبط؟
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # لو فلاش موجود نختاره، لو لا ناخد أول واحد متاح
        for m in models:
            if 'gemini-1.5-flash' in m: return m
        return models[0] if models else 'gemini-pro'
    except Exception:
        return 'gemini-1.5-flash'

# تشغيل الموديل المكتشف
working_model = find_my_model()
model = genai.GenerativeModel(working_model)

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
            # طلب المحتوى
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # لو فشل، بنطبع الموديل اللي حاولنا نكلمه عشان نفهم السبب
            st.error(f"فشل الاتصال بـ {working_model}")
            st.write(f"التفاصيل: {e}")
