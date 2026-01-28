import streamlit as st
import requests

st.set_page_config(page_title="SALEH AI PRO", page_icon="👑")

NEW_API_KEY = "AIzaSyAap0wkUBLjvHgmKe4sfil8FWgoc3Tfp5M"

st.title("👑 SALEH AI - ULTIMATE")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.markdown(message["content"])

# دالة للبحث عن الموديل الشغال فعلياً في حسابك
def find_any_working_model():
    # بنسأل جوجل عن القائمة المتاحة لك
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={NEW_API_KEY}"
    try:
        response = requests.get(url)
        models_data = response.json()
        # بنور على أي موديل بيدعم generateContent
        for m in models_data.get('models', []):
            if 'generateContent' in m.get('supportedGenerationMethods', []):
                return m['name'] # هيرجع حاجة زي models/gemini-1.5-flash-latest
        return "models/gemini-pro" # احتياطي
    except:
        return "models/gemini-pro"

if prompt := st.chat_input("اسأل صالح AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        working_model = find_any_working_model()
        # نداء الموديل اللي لقيناه شغال
        url = f"https://generativelanguage.googleapis.com/v1beta/{working_model}:generateContent?key={NEW_API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            res = requests.post(url, json=payload)
            data = res.json()
            if res.status_code == 200:
                ans = data['candidates'][0]['content']['parts'][0]['text']
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            else:
                st.error(f"جوجل لسه معاندة! الموديل اللي لقيناه هو {working_model} بس مش راضي يرد.")
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
