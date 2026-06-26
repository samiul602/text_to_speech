import streamlit as st
from file_handler import extract_text_from_pdf, extract_text_from_txt
from tts_engine import offline_tts, online_tts

# ── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(page_title="Text to Speech", page_icon="🔊", layout="centered")

# ── Session State Init ─────────────────────────────────────────────────────
if "text" not in st.session_state:
    st.session_state.text = ""
if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None
if "mime" not in st.session_state:
    st.session_state.mime = None
if "clear" not in st.session_state:
    st.session_state.clear = False


if "upload_key" not in st.session_state:
    st.session_state.upload_key = 0
# ── Clear Logic ────────────────────────────────────────────────────────────
def clear_all():
    st.session_state.text = ""
    st.session_state.audio_bytes = None
    st.session_state.mime = None
    st.session_state.clear = True
    st.session_state.upload_key += 1
   

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📊 Text Stats")
    char_count = st.empty()
    word_count = st.empty()
    st.divider()
    st.markdown("### ℹ️ About")
    st.markdown("""
    **Text to Speech Converter**  
    Built with Python & Streamlit  
    
    🔊 Supports two TTS engines:
    - **gTTS** — Online, multi-language
    - **pyttsx3** — Offline, speed control
    
    📄 Accepts:
    - Manual text input
    - TXT file upload
    - PDF file upload
    
    ---
    👨‍💻 Developed by **Sami**  
    """)

# ── Main UI ────────────────────────────────────────────────────────────────
st.title("🔊 Text to Speech Converter")
st.markdown("Type text, or upload a **TXT / PDF** file — then convert it to speech!")

# ── Input Section ──────────────────────────────────────────────────────────
st.subheader("📝 Input Text")

input_method = st.radio("Choose input method:", ["Type Text", "Upload File"], horizontal=True)

text = ""

if input_method == "Type Text":
    text = st.text_area(
        "Enter your text here:",
        height=200,
        placeholder="Type something...",
        value="" if st.session_state.clear else st.session_state.text,
        key="text_input"
    )
    st.session_state.text = text
    st.session_state.clear = False

else:
    uploaded_file = st.file_uploader("Upload a TXT or PDF file:", type=["txt", "pdf"], key=f"uploader_{st.session_state.upload_key}")
    if uploaded_file:
        st.session_state.clear = False
        if uploaded_file.name.endswith(".pdf"):
            text = extract_text_from_pdf(uploaded_file)
        else:
            text = extract_text_from_txt(uploaded_file)
        st.session_state.text = text
        st.success("✅ File loaded successfully!")
        st.text_area("Extracted Text:", value=text, height=200)

text = st.session_state.text

# ── Update Sidebar Stats ───────────────────────────────────────────────────
if text.strip():
    char_count.metric("Characters", len(text))
    word_count.metric("Words", len(text.split()))
else:
    char_count.metric("Characters", 0)
    word_count.metric("Words", 0)

# ── TTS Settings ───────────────────────────────────────────────────────────
st.subheader("⚙️ Settings")

engine = st.selectbox("Choose TTS Engine:", ["Online (gTTS — better quality)", "Offline (pyttsx3 — no internet)"])

if "Online" in engine:
    lang = st.selectbox("Language:", [
        "en — English",
        "bn — Bangla",
        "hi — Hindi",
        "ar — Arabic",
        "fr — French",
        "de — German",
        "zh — Chinese",
    ])
    lang_code = lang.split(" — ")[0]
    slow = st.checkbox("Slow Speed", value=False)
else:
    speed = st.slider("Speech Speed (words per minute):", min_value=50, max_value=300, value=150, step=10)

# ── Buttons ────────────────────────────────────────────────────────────────
st.subheader("🎧 Output")

col1, col2 = st.columns([3, 1])

with col1:
    convert_btn = st.button("🔊 Convert to Speech", use_container_width=True)
with col2:
    clear_btn = st.button("🗑️ Clear", use_container_width=True, on_click=clear_all)

# ── Convert Logic ──────────────────────────────────────────────────────────
if convert_btn:
    if not text.strip():
        st.warning("⚠️ Please enter or upload some text first!")
    else:
        with st.spinner("Converting..."):
            try:
                if "Online" in engine:
                    audio_bytes, mime = online_tts(text, lang=lang_code, speed=slow)
                else:
                    audio_bytes, mime = offline_tts(text, speed=speed)

                st.session_state.audio_bytes = audio_bytes
                st.session_state.mime = mime

            except Exception as e:
                st.error(f"❌ Error: {e}")

# ── Audio Output ───────────────────────────────────────────────────────────
if st.session_state.audio_bytes:
    st.audio(st.session_state.audio_bytes, format=st.session_state.mime)
    ext = "mp3" if st.session_state.mime == "audio/mp3" else "wav"
    st.download_button(
        label=f"⬇️ Download Audio (.{ext})",
        data=st.session_state.audio_bytes,
        file_name=f"output.{ext}",
        mime=st.session_state.mime,
        use_container_width=True
    )
    st.success("✅ Done!")