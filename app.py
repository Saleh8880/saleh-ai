import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="SALEH AI", page_icon="👑")

# ستايل ذهبي وفخم
st.markdown("""
    <style>
    .main { background: #000; }
    .stChatFloatingInputContainer { bottom: 20px; }
    div[data-testid="stChatMessage"] { background: #111; border: 1px solid #D4AF37; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("👑 SALEH AI - PRO")

# إعداد API
API_KEY = "AIzaSyD3VJe5eS8WyZpdo98wu9MywGgbks3K2us"
genai.configure(api_key=API_KEY)

# وظيفة للبحث عن الموديل الشغال تلقائياً
@st.cache_resource
def get_working_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # بنختار فلاش لو موجود لأنه الأسرع
                if 'gemini-1.5-flash' in m.name:
                    return m.name
        return 'models/gemini-pro' # كخيار احتياطي
    except:
        return 'gemini-1.5-flash'

model_name = get_working_model()
model = genai.GenerativeModel(model_name)

# ذاكرة الشات
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة الإدخال
if prompt := st.chat_input("اسألني AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            full_response = response.text
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
            st.info("حاول تحديث الصفحة أو التأكد من إعدادات الـ API")
