import streamlit as st
from google import genai
from google.genai import types
import PIL.Image

# --- 1. API Configuration ---
API_KEY = "AIzaSyCPjbLBC3p_3jgeKmdSU2LqzVM9xzu0218"
client = genai.Client(api_key=API_KEY)

# --- 2. Specialist System Instruction ---
SYSTEM_PROMPT = """
You are 'Euler-Gemini,' an elite mathematical authority specialized in IMO (International Mathematical Olympiad) standards.
CORE OPERATING PRINCIPLES:
1. RIGOR: Provide formal proofs. Use lemmas where necessary.
2. LATEX: Wrap all math in $...$ for inline and $$...$$ for blocks.
3. DOMAIN EXPERTISE: Euclidean Geometry, Number Theory, Combinatorics, Algebra.
4. PROPOSER MODE: Generate unique problems with a marking scheme (0-7 points).
"""

# --- 3. Streamlit UI Setup ---
st.set_page_config(page_title="Math-specialized Chatbot", layout="wide")

# Initialize Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Sidebar for Customization & Uploads ---
with st.sidebar:
    st.header("👤 Profile Settings")
    # Button to upload your personal photo
    profile_photo = st.file_uploader("Upload your profile photo", type=['png', 'jpg', 'jpeg'], key="profile")
    
    # NEW: Customization slider for photo size
    photo_size = st.slider("Customize Photo Size", min_value=50, max_value=500, value=200, step=10)
    
    st.divider()
    
    st.header("📐 Math Exploration")
    # Button to upload math problem diagrams
    math_file = st.file_uploader("Upload Math Diagram", type=['png', 'jpg', 'jpeg'], key="math_prob")
    if math_file:
        st.image(math_file, caption="Input Data")
    
    if st.button("Clear History"):
        st.session_state.chat_history = []
        st.rerun()

# --- Header Layout ---
# Adjusted column ratio to 70/30 to give the photo more room if it gets large
col1, col2 = st.columns([0.7, 0.3]) 

with col1:
    st.title("📐 Math Problem-Solving Chatbot")
    st.markdown("Personal-learning Chatbot with **V. Pichkanika** | Gemini 3.1 Architecture")

with col2:
    if profile_photo:
        # Uses the slider value 'photo_size' for width
        st.image(profile_photo, width=photo_size)
    else:
        st.warning("Upload photo in sidebar")

st.divider()

# --- 4. Chat Interface ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Input your math problem..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            current_contents = [prompt]
            if math_file:
                img = PIL.Image.open(math_file)
                current_contents.append(img)

            response = client.models.generate_content(
                model="gemini-3-flash-preview", 
                contents=current_contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.1,
                    max_output_tokens=2048
                )
            )
            
            answer_text = response.text
            st.markdown(answer_text)
            st.session_state.chat_history.append({"role": "assistant", "content": answer_text})
            
        except Exception as e:
            st.error(f"API Error: {e}")