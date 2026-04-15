import streamlit as st
from groq import Groq

# 1. Page Config
st.set_page_config(page_title="Medi-Assistant AI", page_icon="💊")

# 2. Shoktishali CSS (Ja niche thaka sob button totaly hide korbe)
hide_everything_permanently = """
    <style>
    /* Main Menu, Header, ebong Footer hide kora */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display:none !important;}
    
    /* Hosted with Streamlit (Red Bar) ebong Profile Icon hide kora.
       Ekhane 'display: none' er sathe 'important' use kora hoyeche jate kew na dekhe.
    */
    [data-testid="stStatusWidget"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Sob dhoroner toolbar ebong decoration hide kora */
    [data-testid="stToolbar"] {visibility: hidden !important;}
    [data-testid="stDecoration"] {display:none !important;}

    /* Screen-er niche kono clicking area rakha jabe na */
    .stApp > header {
        display: none !important;
    }
    
    /* Extra layer safety jate scroll korleo kichu na ashe */
    .viewerBadge_container__1QSob {
        display: none !important;
    }
    </style>
    """
st.markdown(hide_everything_permanently, unsafe_allow_html=True)

st.title("🤖 Medi-Assistant AI")
st.markdown("---")

# Groq Connection
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Secrets-e GROQ_API_KEY khuje paoya jayni!")
    st.stop()

# Sidebar Setup
with st.sidebar:
    st.header("📄 Medical Records / Research")
    uploaded_file = st.file_uploader("Fikashun ba research file upload korun...", type=['png', 'jpg', 'jpeg', 'pdf'])
    if uploaded_file is not None:
        st.success(f"File: {uploaded_file.name} upload hoyeche!")
    
    st.info("Ami apnake oushudh, genetic engineering ebong shastho bishoyok tathy diye shahajjo korte pari.")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input & AI Response
if prompt := st.chat_input("Oushudh ba shastho niye kichu jiggesha korun..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            system_instruction = {
                "role": "system", 
                "content": "You are Medi-Assistant AI. Specialized in Biotechnology and Medical info. Answer in Bengali if needed. Always provide medical disclaimer."
            }
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[system_instruction] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )
            
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Sorry, ekta somossya hoyeche: {e}")

st.markdown("---")
st.caption("⚠️ Eti ekti AI shahajhokari. Guruttorpurno proyojone daktarer poramorsho nin.")
