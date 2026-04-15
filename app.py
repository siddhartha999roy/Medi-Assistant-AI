import streamlit as st
from groq import Groq

# ১. পেজ সেটআপ
st.set_page_config(page_title="Medi-Assistant AI", page_icon="💊")

# ২. আলটিমেট হাইড এবং ক্লিক ব্লক করার CSS
# এটি বাটন দুটিকে একদম অদৃশ্য (Total Hide) করে দেবে
hide_st_style = """
    <style>
    /* সব ডিফল্ট এলিমেন্ট হাইড করা */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stAppDeployButton {display:none !important;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    [data-testid="stDecoration"] {display:none !important;}

    /* ৩. নিচের 'Hosted with Streamlit' এবং প্রোফাইল সেকশন পুরোপুরি হাইড করা */
    /* আমরা ক্লাস এবং টেস্ট-আইডি উভয়কেই টার্গেট করছি */
    div[data-testid="stStatusWidget"], 
    .viewerBadge_container__1QSob, 
    div[class*="viewerBadge"] {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
    }
    
    /* নিচের সাদা ফাঁকা অংশ কমানোর জন্য */
    .block-container {
        padding-bottom: 0rem !important;
    }
    
    /* অ্যাপের বডি থেকে স্ক্রলবার ব্যালেন্স করা */
    .stApp {
        bottom: 0 !important;
    }
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("🤖 Medi-Assistant AI")
st.markdown("---")

# Groq চাবি কানেক্ট করা
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Secrets-এ GROQ_API_KEY খুঁজে পাওয়া যায়নি!")
    st.stop()

# সাইডবারে ফাইল আপলোড সেকশন
with st.sidebar:
    st.header("📄 Medical Records / Research")
    uploaded_file = st.file_uploader("প্রেসক্রিপশন বা রিসার্চ ফাইল আপলোড করুন...", type=['png', 'jpg', 'jpeg', 'pdf'])
    if uploaded_file is not None:
        st.success(f"ফাইল: {uploaded_file.name} আপলোড হয়েছে!")
    st.info("আমি আপনাকে ওষুধ এবং জেনেটিক ইঞ্জিনিয়ারিং বিষয়ক তথ্য দিয়ে সাহায্য করতে পারি।")

# চ্যাট হিস্ট্রি মেনটেইন করা
if "messages" not in st.session_state:
    st.session_state.messages = []

# পুরনো মেসেজগুলো প্রদর্শন করা
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ইউজার ইনপুট এবং AI রেসপন্স
if prompt := st.chat_input("ওষুধ বা স্বাস্থ্য নিয়ে কিছু জিজ্ঞাসা করুন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            system_instruction = {
                "role": "system", 
                "content": "You are Medi-Assistant AI. Specialized in Biotechnology and Medical information. Answer in Bengali if needed. Always provide medical disclaimer."
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
            st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")

st.markdown("---")
st.caption("⚠️ এটি একটি AI সাহায্যকারী। গুরুতর প্রয়োজনে অভিজ্ঞ ডাক্তারের পরামর্শ নিন।")
