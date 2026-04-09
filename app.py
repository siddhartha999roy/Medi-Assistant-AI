import streamlit as st
import google.generativeai as genai

# ১. পেজ সেটআপ (ব্রাউজার ট্যাবে যা দেখাবে)
st.set_page_config(page_title="Global Student AI", page_icon="🎓")
st.title("🎓 Global Student AI")

# ২. সিক্রেট চাবি (API Key) কানেক্ট করা
# এটি আপনার Streamlit Settings > Secrets থেকে GOOGLE_API_KEY খুঁজে নেবে
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
else:
    st.error("API Key খুঁজে পাওয়া যায়নি! দয়া করে Streamlit Secrets চেক করুন।")
    st.stop()

# ৩. এআই মডেল সেটআপ (Flash মডেলটি দ্রুত কাজ করে)
model = genai.GenerativeModel('gemini-1.5-flash')

# ৪. চ্যাট হিস্ট্রি বা মেসেজ মনে রাখার ব্যবস্থা
if "messages" not in st.session_state:
    st.session_state.messages = []

# ৫. আগের কথাগুলো স্ক্রিনে দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৬. ইউজার ইনপুট বক্স এবং উত্তর জেনারেশন
if prompt := st.chat_input("Ask me anything..."):
    # ইউজারের মেসেজ সেভ করা এবং দেখানো
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # এআই-এর উত্তর তৈরি করা
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            # এআই-এর উত্তর সেভ করা
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # কোটা শেষ হলে বা অন্য সমস্যা হলে এই এরর দেখাবে
            st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")
