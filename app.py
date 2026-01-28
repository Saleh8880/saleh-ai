import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SALEH AI", page_icon="👑")

# ستايل فخم
st.markdown("""
    <style>
    .main { background: #000; }
    div[data-testid="stChatMessage"] { background: #111; border: 1px solid #D4AF37; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("👑 SALEH AI - PRO")

# إعداد API
# ملاحظة: إذا استمر الخطأ، قد تحتاج لإنشاء مفتاح جديد من Google AI Studio
API_KEY = "AIzaSyD3VJe5eS8WyZpdo98wu9MywGgbks3K2us"
genai.configure(api_key=API_KEY)

# استخدام الموديل بالاسم المباشر وبدون تحديد إصدار v1beta يدوياً
# جربنا gemini-1.5-flash كأكثر موديل مستقر حالياً
model = genai.GenerativeModel('gemini-1.5-flash')

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
            # محاولة توليد محتوى
            response = model.generate_content(prompt)
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("جوجل استلم الطلب بس مبعتش نص. جرب سؤال تاني.")
        except Exception as e:
            st.error(f"خطأ في الاتصال: {e}")
            st.info("نصيحة: إذا استمر الخطأ، جرب إنشاء مفتاح API جديد من Google AI Studio وضعه في الكود.")
