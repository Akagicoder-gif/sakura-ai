import streamlit as st
from huggingface_hub import InferenceClient
from PIL import Image
import io

# --- 🌸 SAKURA'S KEY 🌸 ---
import streamlit as st
client = InferenceClient(api_key=st.secrets["HF_TOKEN"])

st.set_page_config(page_title="Sakura AI", page_icon="🌸")
st.title("🌸 Sakura AI")
st.write("Welcome, I am Sakura, your personal AI.")

# --- SIDEBAR FOR IMAGE GENERATION ---
st.sidebar.header("Paint with Sakura")
image_prompt = st.sidebar.text_input("What should Sakura draw?")
if st.sidebar.button("Generate Image"):
    if image_prompt:
        with st.spinner("Sakura is painting..."):
            image = client.text_to_image(image_prompt, model="stabilityai/stable-diffusion-xl-base-1.0")
            st.sidebar.image(image, caption=f"Sakura's drawing of: {image_prompt}")
    else:
        st.sidebar.warning("Please tell Sakura what to draw first!")

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add a button to clear memory if she gets confused
if st.sidebar.button("Clear Chat Memory"):
    st.session_state.messages = []
    st.rerun()

# Show previous messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Talk to Sakura..."):
    # 1. Add your message with the Star icon
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🌟"):
        st.markdown(prompt)

    # 2. Sakura replies with the Flower icon
    with st.chat_message("assistant", avatar="🌸"):
        response_placeholder = st.empty()
        full_response = ""
        
        messages_to_send = [
            {"role": "system", "content": "You are Sakura, a friendly and cheerful AI. Answer briefly!"}
        ] + st.session_state.messages[-6:]

        for chunk in client.chat.completions.create(
            model="HuggingFaceH4/zephyr-7b-beta",
            messages=messages_to_send,
            max_tokens=500,
            stream=True,
        ):
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
    
    # 3. Save her answer to memory
    st.session_state.messages.append({"role": "assistant", "content": full_response})