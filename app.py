import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SALEH AI GOLD", page_icon="👑")

# المفاتيح اللي معاك
api_keys = [
    "AIzaSyA83bkpXNvLB7bmcqOpDi7ucGYqI7K7kD4",
    "AIzaSyCRGxh0HeSmv0QV3BP65yMuWiltDxEskl4"
]

if "key_index" not in st.session_state:
    st.session_state.key_index = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("👑 SALEH AI - ULTIMATE")

# عرض الشات
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسأل صالح AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        success = False
        for _ in range(len(api_keys)):
            try:
                # ضبط المفتاح الحالي
                genai.configure(api_key=api_keys[st.session_state.key_index])
                
                # الحل هنا: استخدام الاسم المختصر للموديل
                # لو فلاش مانفعش، الكود هيجرب 'gemini-pro' أوتوماتيك
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(prompt)
                except:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(prompt)

                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                success = True
                break
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg: # ضغط رسايل
                    st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
                    continue
                else:
                    st.error(f"تنبيه فني: {error_msg}")
                    break
        
        if not success:
            st.info("صالح، جرب تعمل ريفريش (Refresh) للصفحة، السيرفر بيحدث بيانات المفاتيح.")
