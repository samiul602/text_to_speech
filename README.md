# 🔊 Text to Speech Converter

🔗 **Live App:**https://text2speech-sami.streamlit.app/

A Streamlit web app that converts text to speech using two TTS engines.

## Features
- ✍️ Type text manually
- 📄 Upload TXT or PDF file
- 🌍 Multiple languages (English, Bangla, Hindi, Arabic, French, German, Chinese)
- ⚙️ Two TTS engines — Online (gTTS) & Offline (pyttsx3)
- ⬇️ Download audio as MP3 or WAV
- 🗑️ Clear button to reset everything

## How to Run

```bash
# 1 — Clone the repo
git clone https://github.com/samiul602/text_to_speech.git
cd text_to_speech

# 2 — Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3 — Install dependencies
pip install -r requirements.txt

# 4 — Run the app
streamlit run app.py
```

## Tech Stack
- Python 3.11
- Streamlit
- gTTS
- pyttsx3
- PyMuPDF

## Developed by
**Sami** 