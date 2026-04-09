import streamlit as st
from groq import Groq

# পেজ সেটআপ
st.set_page_config(page_title="Global Student AI", page_icon="🎓")
st.title("🎓 Global Student AI")

# Groq চাবি কানেক্ট করা
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Secrets-এ GROQ_API_KEY খুঁজে পাওয়া যায়নি!")
    st.stop()

# সাইডবারে ইমেজ আপলোড অপশন
with st.sidebar:
    st.header("Upload Section")
    uploaded_file = st.file_uploader("Choose a picture or PDF...", type=['png', 'jpg', 'jpeg', 'pdf'])
    if uploaded_file is not None:
        st.success("File uploaded successfully!")

# চ্যাট হিস্ট্রি
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ইউজার ইনপুট
if prompt := st.chat_input("Ask about Genetic Engineering..."):
    # ফাইলের তথ্য প্রম্পটের সাথে যোগ করা (যদি ফাইল থাকে)
    full_prompt = prompt
    if uploaded_file:
        full_prompt = f"User has uploaded a file: {uploaded_file.name}. \nQuestion: {prompt}"

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
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
