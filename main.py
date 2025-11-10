import streamlit as st
import re
from io import BytesIO

# --- Function to remove Markdown syntax (supports tables + text) ---
def remove_markdown(text):
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)   # code blocks
    text = re.sub(r'`([^`]*)`', r'\1', text)                # inline code
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)             # images
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)    # links
    text = re.sub(r'(\*{1,2}|_{1,2})(.*?)\1', r'\2', text)  # bold/italic
    text = re.sub(r'^(#{1,6})\s*', '', text, flags=re.MULTILINE)  # headings
    text = re.sub(r'^>\s?', '', text, flags=re.MULTILINE)   # blockquotes
    text = re.sub(r'^[-*_]{3,}\s*$', '', text, flags=re.MULTILINE) # hr
    text = re.sub(r'\|[ \t]*-+[ \t]*\|', '|', text)         # table dividers
    text = re.sub(r'\|\s*', '', text)                       # table pipes
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)   # bullet lists
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)   # numbered lists
    text = re.sub(r'\n{2,}', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

# --- Streamlit Config ---
st.set_page_config(page_title="Markdown Remover", page_icon="🧹", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
        /* Background gradient */
        body {
            background: linear-gradient(135deg, #dbeafe, #ecfccb, #fef3c7);
            background-attachment: fixed;
        }
        /* Glassmorphism main container */
        .block-container {
            max-width: 800px;
            margin: 3rem auto;
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(15px);
            padding: 2.5rem 2rem;
            border-radius: 25px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            background: linear-gradient(90deg, #2563eb, #16a34a);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            letter-spacing: 1px;
        }
        .stTabs [data-baseweb="tab-list"] {
            justify-content: center;
            background-color: #f8fafc;
            border-radius: 12px;
            margin-bottom: 1rem;
        }
        .stTabs [data-baseweb="tab"] {
            font-weight: 600;
            color: #1e3a8a;
        }
        .stButton button {
            background: linear-gradient(90deg, #2563eb, #16a34a);
            color: white;
            border-radius: 12px;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            border: none;
            transition: 0.3s;
        }
        .stButton button:hover {
            transform: scale(1.03);
            box-shadow: 0 4px 15px rgba(37,99,235,0.3);
        }
        .stDownloadButton button {
            background: linear-gradient(90deg, #14b8a6, #06b6d4);
            color: white;
            border-radius: 12px;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            border: none;
            transition: 0.3s;
        }
        .stDownloadButton button:hover {
            transform: scale(1.03);
            box-shadow: 0 4px 15px rgba(20,184,166,0.3);
        }
        .stTextArea textarea {
            border-radius: 12px;
            font-family: 'Courier New', monospace;
            background-color: #f9fafb;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1>🧹 Markdown Remover</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#475569;'>Remove Markdown syntax effortlessly — paste or upload your file and get clean, plain text instantly.</p>", unsafe_allow_html=True)

# --- Tabs ---
tab1, tab2 = st.tabs(["📝 Paste Markdown/Text", "📁 Upload File (.md or .txt)"])

with tab1:
    markdown_input = st.text_area(
        "Enter Markdown or Text",
        height=250,
        placeholder="### Example:\n| Name | Age |\n|------|-----|\n| Alice | 24 |\n| Bob | 30 |"
    )
    process_btn = st.button("🧼 Remove Markdown (Text Input)")

with tab2:
    uploaded_file = st.file_uploader("Drag & drop or choose a Markdown/Text file", type=["md", "markdown", "txt"])
    process_file_btn = st.button("🧼 Remove Markdown (Uploaded File)")

# --- Processing ---
if process_btn and markdown_input.strip():
    cleaned_text = remove_markdown(markdown_input)
    st.success("✅ Markdown removed successfully!")
    st.text_area("Cleaned Text", cleaned_text, height=250)
    download = BytesIO(cleaned_text.encode())
    st.download_button("📥 Download Cleaned Text", download, "cleaned_text.txt", "text/plain")

elif process_file_btn and uploaded_file:
    markdown_input = uploaded_file.read().decode("utf-8", errors="ignore")
    cleaned_text = remove_markdown(markdown_input)
    st.success(f"✅ Markdown removed successfully from {uploaded_file.name}")
    st.text_area("Cleaned Text", cleaned_text, height=250)
    download = BytesIO(cleaned_text.encode())
    st.download_button("📥 Download Cleaned Text", download, f"{uploaded_file.name}_cleaned.txt", "text/plain")

elif (process_btn and not markdown_input.strip()) or (process_file_btn and not uploaded_file):
    st.warning("⚠️ Please enter some text or upload a file first.")
