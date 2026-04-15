import streamlit as st
from groq import Groq

st.set_page_config(page_title="Medi-Assistant AI", page_icon="💊")

# উন্নত CSS - চ্যাট বক্স ওপরে তোলা হয়েছে
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display:none;}
    [data-testid="stStatusWidget"] {display: none !important;}
    
    /* চ্যাট ইনপুট ১৫ পিক্সেল ওপরে তোলা হয়েছে */
    [data-testid="stChatInput"] {
        bottom: 15px !important;
    }
    
    .block-container {
        padding-bottom: 3.5rem !important;
    }
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("🤖 Medi-Assistant AI")

if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("GROQ_API_KEY Missing!")
    st.stop()

with st.sidebar:
    st.header("📄 Medical Records")
    uploaded_file = st.file_uploader("Upload file...", type=['png', 'jpg', 'jpeg', 'pdf'])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("ওষুধ বা স্বাস্থ্য নিয়ে কিছু জিজ্ঞাসা করুন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            system_instruction = {"role": "system", "content": "You are Medi-Assistant AI. Specialized in Biotechnology. Answer in Bengali if asked."}
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[system_instruction] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("⚠️ অভিজ্ঞ ডাক্তারের পরামর্শ নিন।")
