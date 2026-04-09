import streamlit as st
from groq import Groq

# পেজ কনফিগারেশন
st.set_page_config(page_title="Global Student AI", page_icon="🎓")
st.title("🎓 Global Student AI")

# Groq ক্লায়েন্ট সেটআপ
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Secrets-এ GROQ_API_KEY খুঁজে পাওয়া যায়নি!")
    st.stop()

# চ্যাট হিস্ট্রি মেনটেইন করা
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ইউজার ইনপুট
if prompt := st.chat_input("Ask about Genetic Engineering..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Llama 3 70B মডেলটি অনেক শক্তিশালী
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")
