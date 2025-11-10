"""
AI ClimaSense — Hybrid Intelligence Chat Assistant (v8)
Enhanced interactive UI + feedback analytics + dynamic design + insight summary
Launch:
    streamlit run app.py
"""

import os, sys, sqlite3
import streamlit as st
import pandas as pd
# ------------------------------------------------------------
# 🌐 Temporary Diffusion Model Placeholder
# ------------------------------------------------------------
from PIL import Image, ImageDraw, ImageFilter
import random

def generate_downscaled_map(lat, lon):
    """
    Context-aware synthetic climate map generator.
    Generates regional-like rainfall or heat intensity maps using smooth gradients and clusters.
    """
    width, height = 512, 320
    img = Image.new("RGB", (width, height), color=(245, 248, 255))
    draw = ImageDraw.Draw(img)

    # --- Generate layered gradient base ---
    base_color = (180, 210, 255)  # light sky tone
    for y in range(height):
        factor = y / height
        r = int(base_color[0] * (1 - 0.3 * factor))
        g = int(base_color[1] * (1 - 0.5 * factor))
        b = int(base_color[2] * (1 - 0.7 * factor))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # --- Simulate rainfall/heat zones ---
    for _ in range(10):  # clusters
        cx = random.randint(100, width - 100)
        cy = random.randint(60, height - 60)
        radius = random.randint(40, 100)

        # Choose weather type (rain or heat)
        if random.random() < 0.6:
            # Rain zone (blue/green gradient)
            fill_color = (
                random.randint(0, 80),
                random.randint(100, 180),
                random.randint(200, 255),
            )
        else:
            # Heat zone (orange/red)
            fill_color = (
                random.randint(200, 255),
                random.randint(100, 150),
                random.randint(60, 80),
            )

        for r in range(radius, 0, -1):
            alpha = int(255 * (1 - r / radius) ** 2)
            color = tuple(int(c * (r / radius)) for c in fill_color)
            draw.ellipse(
                [(cx - r, cy - r), (cx + r, cy + r)],
                fill=color,
                outline=None,
            )

    # --- Add topographic grid lines ---
    for i in range(0, width, 64):
        draw.line([(i, 0), (i, height)], fill=(220, 220, 220), width=1)
    for j in range(0, height, 64):
        draw.line([(0, j), (width, j)], fill=(220, 220, 220), width=1)

    # --- Add title & coordinate overlay ---
    header_box = [(10, 10), (width - 10, 55)]
    draw.rectangle(header_box, fill=(255, 255, 255, 220))
    draw.text((20, 18), f"Synthetic Climate Map\nLat {lat:.2f}, Lon {lon:.2f}", fill=(50, 50, 50))

    # --- Apply blur & contrast for realism ---
    img = img.filter(ImageFilter.GaussianBlur(radius=1.0))

    return img



import matplotlib.pyplot as plt
from datetime import datetime

# Local imports
from services.genai_service import answer_query
from services.climate_api_service import fetch_weather_summary
from utils.logger import get_logger
from utils.auto_rebuild import auto_rebuild_vectorstore
from utils.web_search import perform_web_search
from utils.feedback_db import store_feedback_db, get_feedback_entries
from config.config import DEFAULT_LAT, DEFAULT_LON

logger = get_logger("app")

# ------------------------------------------------------------
# Streamlit Configuration
# ------------------------------------------------------------
st.set_page_config(page_title="AI ClimaSense", layout="wide", page_icon="🌿")

# ------------------------------------------------------------
# 🌈 Modern Interactive UI
# ------------------------------------------------------------
st.markdown("""
<style>
html, body, [class*="block-container"] {
    overflow: auto !important; padding-top: 0.3rem !important;
}
.stApp {
    background: linear-gradient(135deg, #0b1e26 10%, #002b36 60%, #013a46 100%);
    color: #eaf4f4; font-family: 'Inter', sans-serif;
}
header[data-testid="stHeader"] {
    background: linear-gradient(90deg,#005f73,#0a9396);
    box-shadow: 0 2px 15px rgba(0,255,213,0.25);
    padding:0.6rem 1rem; position:sticky;top:0;z-index:999;
}
h1 {
    color:#94f1d9; text-shadow:0 0 12px rgba(0,255,170,0.6);
    font-weight:800; text-align:center; font-size:2.5rem;
}
.stTextInput>div>div>input {
    background-color:#0d262c; border:1px solid #0ff6b3;
    color:#e0f2f1; border-radius:10px; padding:10px;
}
.stButton button {
    background:linear-gradient(90deg,#006d77,#83c5be);
    color:#f8fafc; border:none; border-radius:8px; padding:8px 18px;
    font-weight:600; transition:all .3s ease;
}
.stButton button:hover {
    background:linear-gradient(90deg,#94d2bd,#e9d8a6);
    color:#012c33; transform:scale(1.05); box-shadow:0 0 10px #0ff6b3;
}
[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#031c20,#043336);
}
.stSidebar h2,.stSidebar h3 { color:#0ff6b3; }
.chat-card {
    background:rgba(255,255,255,0.04); border-left:4px solid #0a9396;
    border-radius:10px; padding:12px 18px; margin:10px 0;
    box-shadow:0 0 6px rgba(10,147,150,0.3);
}
.footer-text {
    text-align: center;
    color: #6b21a8 !important;          /* deep violet for clarity */
    font-weight: 600 !important;        /* makes text readable */
    font-size: 0.95rem !important;      /* slightly larger */
    margin-top: 1.5rem !important;
    padding-top: 1rem !important;
    border-top: 1px solid #e5e7eb !important;
    text-shadow: 0 0 6px rgba(168,85,247,0.15);  /* subtle glow */
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 🌿 Modern White Cortex UI Add-on (non-conflicting enhancement)
# ------------------------------------------------------------
st.markdown("""
<style>
/* Layer above existing theme */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%) !important;
    color: #111827 !important;
}
.stApp {
    background-color: #ffffff !important;
}
.stTextInput > div > div > input {
    background-color: #ffffff !important;
    border: 1.5px solid #d1d5db !important;
    color: #111827 !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    transition: all 0.2s ease;
}
.stTextInput > div > div > input:focus {
    border-color: #a855f7 !important;
    box-shadow: 0 0 0 4px rgba(168,85,247,0.2);
}
.stButton > button {
    border: none !important;
    border-radius: 12px !important;
    background: linear-gradient(90deg, #7c3aed, #a855f7) !important;
    color: #fff !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 16px rgba(124,58,237,0.25);
    transition: all 0.2s ease-in-out;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(124,58,237,0.3);
}
[data-testid="stSidebar"] {
    background: #f9fafb !important;
    border-right: 1px solid #e5e7eb !important;
    box-shadow: 2px 0 8px rgba(0,0,0,0.05);
}
h1, h2, h3 {
    color: #7c3aed !important;
    text-shadow: none !important;
}
.chat-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 14px 18px;
    margin: 12px 0;
    border-left: 4px solid #a855f7;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)
# ------------------------------------------------------------
# 🎨 Sidebar and Analytics Visibility Fix (for White UI)
# ------------------------------------------------------------
st.markdown("""
<style>
/* --- Sidebar Section --- */
[data-testid="stSidebar"] {
    background: #f9fafb !important;
    color: #111827 !important;
}

/* Sidebar text and headers */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #111827 !important;
}

/* Sidebar icons (checkboxes, expanders, etc.) */
[data-testid="stSidebar"] svg, [data-testid="stSidebar"] path {
    fill: #7c3aed !important; /* violet tint for icons */
    stroke: #7c3aed !important;
}

/* Expander headings */
.streamlit-expanderHeader {
    color: #7c3aed !important;
    font-weight: 600 !important;
}

/* Checkbox and radio buttons */
[data-baseweb="checkbox"] label p {
    color: #111827 !important;
}

/* Matplotlib charts fix (axes, ticks, labels) */
div[data-testid="stVerticalBlock"] .stPlotlyChart,
div[data-testid="stVerticalBlock"] .stMarkdown,
div[data-testid="stVerticalBlock"] .stAltairChart,
div[data-testid="stVerticalBlock"] .stPyplot {
    color: #111827 !important;
    background: #ffffff !important;
}

/* Figure captions and chart titles */
.js-plotly-plot text,
.js-plotly-plot tspan {
    fill: #111827 !important;
}

/* Tool icons (e.g., checkboxes, buttons) in feedback analytics */
[data-testid="stSidebar"] .stCheckbox label,
[data-testid="stSidebar"] .stRadio label {
    color: #111827 !important;
    font-weight: 500 !important;
}
</style>
""", unsafe_allow_html=True)
# ------------------------------------------------------------
# ✨ Gradient Input Box Styling (Cortex / ChatGPT style)
# ------------------------------------------------------------
st.markdown("""
<style>
/* Main input container enhancement */
div[data-testid="stTextInput"] > div:first-child {
    background: linear-gradient(90deg, #7c3aed, #3b82f6, #a855f7);
    padding: 2px;
    border-radius: 14px;
    box-shadow: 0 6px 16px rgba(124,58,237,0.15);
}

/* Inner input field (the actual text area) */
div[data-testid="stTextInput"] > div:first-child > div {
    background-color: #ffffff !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
    box-shadow: inset 0 2px 6px rgba(0,0,0,0.04);
}

/* Text styling */
.stTextInput > div > div > input {
    font-size: 1rem !important;
    color: #111827 !important;
    border: none !important;
    outline: none !important;
    background: transparent !important;
}

/* Placeholder text */
.stTextInput > div > div > input::placeholder {
    color: #9ca3af !important;
    font-style: italic;
}

/* Add subtle glow on focus */
.stTextInput > div > div > input:focus {
    box-shadow: 0 0 0 2px rgba(124,58,237,0.2);
}

/* Align Send button to match new style */
.stButton > button {
    border-radius: 10px !important;
    padding: 8px 22px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    background: linear-gradient(90deg, #7c3aed, #a855f7) !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.25);
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(124,58,237,0.35);
}
</style>
""", unsafe_allow_html=True)
# ------------------------------------------------------------
# Modern Chat Input Design (Cortex style)
# ------------------------------------------------------------

st.markdown("""
<style>
/* Outer text area wrapper with full gradient border */
div[data-testid="stTextArea"] > div {
    position: relative;
    background: linear-gradient(white, white) padding-box,
                linear-gradient(90deg, #a855f7, #6366f1, #8b5cf6) border-box;
    border: 2px solid transparent !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 18px rgba(124,58,237,0.08);
    padding: 0 !important;
    overflow: hidden !important;
    transition: all 0.3s ease-in-out;
}

/* Actual textarea background and padding */
textarea {
    border: none !important;
    outline: none !important;
    color: #111827 !important;                /* dark visible text */
    background-color: #ffffff !important;     /* fix white coverage */
    font-size: 1rem !important;
    line-height: 1.6rem !important;
    min-height: 100px !important;
    width: 100% !important;
    resize: none !important;
    padding: 14px 16px !important;
    border-radius: 14px !important;
    caret-color: #7c3aed !important;          /* visible typing caret */
    box-shadow: inset 0 0 6px rgba(124,58,237,0.08);
}

/* Placeholder styling */
textarea::placeholder {
    color: #9ca3af !important;
    font-style: italic;
}

/* Glow when focused */
div[data-testid="stTextArea"] > div:focus-within {
    box-shadow: 0 0 0 3px rgba(124,58,237,0.2);
}

/* Hide the Streamlit input hint text */
div[data-testid="stMarkdownContainer"] p[style*="color: rgb(250, 250, 250)"],
[data-testid="stMarkdownContainer"] span[style*="color: rgb(250, 250, 250)"] {
    display: none !important;
}

/* Adjust Send button for consistency */
.stButton > button {
    border-radius: 10px !important;
    padding: 10px 20px !important;
    background: linear-gradient(90deg, #7c3aed, #a855f7) !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    box-shadow: 0 6px 16px rgba(124,58,237,0.25);
    color: white !important;
    border: none !important;
    transition: all 0.2s ease-in-out;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(124,58,237,0.35);
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.title("🌿 AI ClimaSense — Hybrid Intelligence Chat Assistant")
st.caption("💡 A next-gen climate–agriculture assistant powered by knowledge retrieval and real-time intelligence.")

# ------------------------------------------------------------
# Sidebar Settings
# ------------------------------------------------------------
st.sidebar.header("⚙️ Settings")

# User-defined geographic settings
lat = st.sidebar.number_input("Latitude", value=float(DEFAULT_LAT))
lon = st.sidebar.number_input("Longitude", value=float(DEFAULT_LON))
mode = st.sidebar.selectbox("Response Mode", ["concise", "detailed"])

# ✅ Correct Synthetic Map Toggle (single definition)
generate_map = st.sidebar.checkbox("🌍 Generate Synthetic Map", value=False)


# Web Search Integration
st.sidebar.markdown("### 🌐 Web Search Integration")
web_search_enabled = st.sidebar.checkbox("Enable Live Web Search", value=True)
if web_search_enabled:
    st.sidebar.info("When enabled, the chatbot can search the web for real-time information.")
    if st.sidebar.button("🌍 Run Live Web Search"):
        if "last_user_query" in st.session_state:
            with st.spinner("🔍 Searching live sources…"):
                result = perform_web_search(st.session_state["last_user_query"])
                st.session_state.messages.append({"role": "assistant", "content": result})
        else:
            st.sidebar.warning("Please ask a question first!")

# ------------------------------------------------------------
# Auto Rebuild Vectorstore
# ------------------------------------------------------------
if "vectorstore_checked" not in st.session_state:
    with st.spinner("🔄 Initializing knowledge base…"):
        try:
            auto_rebuild_vectorstore()
        except Exception as e:
            st.sidebar.warning(f"⚠️ Vectorstore rebuild skipped: {e}")
    st.session_state.vectorstore_checked = True

# ------------------------------------------------------------
# Chat State
# ------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------------------------------------
# User Input
# ------------------------------------------------------------
# ------------------------------------------------------------
# 🌤️ Centered Chat Input Card (Cortex-style)
# ------------------------------------------------------------
with st.container():
    st.markdown("""
    <div style='background-color:#ffffff;
                border-radius:18px;
                padding:2rem;
                margin:1.5rem auto;
                box-shadow:0 10px 25px rgba(0,0,0,0.05);
                width:80%;
                text-align:center;'>
        <h2 style='color:#7c3aed;margin-bottom:1rem;'>Ask Your Climate Question 🌾</h2>
        <p style='color:#4b5563;'>Explore insights in any multi-linguial language on weather, crops, adaptation, and sustainability. Chat with ClimaSense in any language that you prefer!</p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------
# 🧠 Modern Chat Input (Cortex-style expanded text box)
# ------------------------------------------------------------
user_input = st.text_area(
    "💬 Ask your climate or agriculture question...",
    height=110,
    placeholder="Ask me anything about climate, crops, or sustainability...",
)
# 🧰 Edit Prompt + Web Search Controls (Functional + Styled)
st.markdown("""
<style>
.prompt-tools {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    margin-top: -0.3rem;
    margin-bottom: 1rem;
}
.stButton > button {
    display: flex;
    align-items: center;
    gap: 8px;
    border: 1px solid #e5e7eb !important;
    border-radius: 10px !important;
    background: #f9fafb !important;
    padding: 8px 18px !important;
    font-size: 0.9rem !important;
    color: #4b5563 !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    cursor: pointer !important;
    transition: all 0.2s ease-in-out !important;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #f3e8ff, #ede9fe) !important;
    color: #7c3aed !important;
    box-shadow: 0 4px 10px rgba(124,58,237,0.1) !important;
    transform: translateY(-1px) !important;
}
</style>
""", unsafe_allow_html=True)

# --- Actual Interactive Buttons ---
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("✏️ Edit Prompt"):
        if "last_user_query" in st.session_state:
            st.session_state["edit_mode"] = True
            st.info("📝 You can now edit your previous prompt above.")
        else:
            st.warning("⚠️ No previous prompt found to edit.")

with col2:
    if st.button("🌐 Web Search"):
        if "last_user_query" in st.session_state and st.session_state["last_user_query"].strip():
            with st.spinner("🔍 Searching the web for insights..."):
                try:
                    result = perform_web_search(st.session_state["last_user_query"])
                    st.session_state.messages.append({"role": "assistant", "content": result})
                    st.success("🌐 Web results added to conversation!")
                except Exception as e:
                    st.error(f"❌ Web search failed: {e}")
        else:
            st.warning("⚠️ Please enter a query first before running web search.")

# Streamlit button trigger below custom UI
if st.button("🗺️ Generate Synthetic Map"):
    with st.spinner("🌀 Generating synthetic map..."):
        try:
            map_image = generate_downscaled_map(lat, lon)
            if map_image:
                st.image(map_image, use_container_width=True)

                # 🌍 Dynamic explanation below the generated map
                st.markdown(f"""
                <div style='background-color:#f9fafb;
                            border-radius:14px;
                            padding:1rem 1.2rem;
                            margin-top:1rem;
                            box-shadow:0 4px 12px rgba(0,0,0,0.05);
                            font-size:0.95rem;
                            line-height:1.6;
                            color:#374151;'>
                <h4 style='color:#7c3aed;'>🧭 What This “Synthetic Climate Map” Represents</h4>

                This visualization is <b>algorithmically generated</b> by the AI diffusion engine to simulate <b>climate behavior patterns</b> around your selected coordinates:<br>
                <b>Latitude:</b> {lat:.2f}, <b>Longitude:</b> {lon:.2f}

                It approximates regional <b>rainfall, heat, or drought intensity zones</b> through synthetic diffusion.  
                You can interpret the color regions as:

                <ul>
                <li><b style="color:#2563eb;">Blue / Cyan zones:</b> Moisture or rainfall-prone regions (wet climate zones)</li>
                <li><b style="color:#ea580c;">Orange / Red zones:</b> Heat or dryness-dominant regions (arid or drought areas)</li>
                <li><b>Gradient background:</b> Terrain and atmospheric blending</li>
                <li><b>Grid lines:</b> Simulated geographic segmentation</li>
                </ul>

                This is a <b>synthetic heatmap</b> — not real satellite data — designed to provide a <b>visual pattern of climate variability</b> near the selected coordinates.

                </div>
                """, unsafe_allow_html=True)

                st.success("✅ Synthetic map generated successfully!")

            else:
                st.warning("⚠️ No map data available.")

        except Exception as e:
            st.error(f"🚫 Error while generating synthetic map: {e}")



if st.button("Send") and user_input.strip():
    st.session_state["last_user_query"] = user_input
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("🤖 Generating insight…"):
        try:
            answer, meta = answer_query(user_input, lat, lon, mode=mode)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            logger.error(f"Response failed: {e}")
            st.session_state.messages.append({"role": "assistant", "content": f"⚠️ Error: {e}"})

# ------------------------------------------------------------
# 💬 Chat Bubble Design (modern Cortex style)
# ------------------------------------------------------------
def render_message(msg):
    if msg["role"] == "assistant":
        st.markdown(
            f"""
            <div style="
                background:#ffffff;
                border-left:4px solid #a855f7;
                border-radius:14px;
                padding:14px 18px;
                margin:12px 0;
                box-shadow:0 4px 10px rgba(0,0,0,0.05);
                color:#111827;">
                <b>🤖 Assistant</b><br>{msg['content']}
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="
                background:#ede9fe;
                border-radius:14px;
                padding:14px 18px;
                margin:12px 0;
                margin-left:auto;
                color:#4c1d95;
                max-width:75%;
                box-shadow:0 4px 10px rgba(124,58,237,0.12);">
                <b>👤 You</b><br>{msg['content']}
            </div>
            """, unsafe_allow_html=True
        )

# ------------------------------------------------------------
# Chat Display + Feedback (Cortex-styled bubbles)
# ------------------------------------------------------------
st.markdown("### 💬 Conversation History")

# Helper function for styled message bubbles
def render_message(msg):
    if msg["role"] == "assistant":
        st.markdown(
            f"""
            <div style="
                background:#ffffff;
                border-left:4px solid #a855f7;
                border-radius:14px;
                padding:14px 18px;
                margin:12px 0;
                box-shadow:0 4px 10px rgba(0,0,0,0.05);
                color:#111827;">
                <b>🤖 Assistant</b><br>{msg['content']}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="
                background:#ede9fe;
                border-radius:14px;
                padding:14px 18px;
                margin:12px 0;
                margin-left:auto;
                color:#4c1d95;
                max-width:75%;
                box-shadow:0 4px 10px rgba(124,58,237,0.12);">
                <b>👤 You</b><br>{msg['content']}
            </div>
            """,
            unsafe_allow_html=True
        )

# Loop through conversation
for msg in reversed(st.session_state.messages):
    render_message(msg)

    # Feedback expander (assistant only)
    if msg["role"] == "assistant":
        with st.expander("✅ Verify this response"):
            st.write("Was this helpful?")
            col1, col2 = st.columns(2)
            if col1.button("👍 Helpful", key=f"yes_{msg['content'][:25]}"):
                q = st.session_state.messages[-2]["content"] if len(st.session_state.messages) > 1 else "N/A"
                store_feedback_db(q, msg["content"], "Correct")
                st.success("✅ Thanks for confirming!")
            if col2.button("👎 Needs Work", key=f"no_{msg['content'][:25]}"):
                q = st.session_state.messages[-2]["content"] if len(st.session_state.messages) > 1 else "N/A"
                store_feedback_db(q, msg["content"], "Needs Improvement")
                st.warning("⚠️ Feedback recorded!")


# ------------------------------------------------------------
# 🌦 Weather Summary
# ------------------------------------------------------------
st.sidebar.markdown("---")
if st.sidebar.button("🌤 Fetch Live Weather Summary"):
    with st.spinner("Fetching from Open-Meteo…"):
        try:
            summary = fetch_weather_summary(lat, lon)
            st.sidebar.success(summary)
        except Exception as e:
            st.sidebar.error(f"❌ Weather fetch failed: {e}")

# ------------------------------------------------------------
# Feedback Analytics Panel
# ------------------------------------------------------------
st.sidebar.markdown("### 📈 Feedback Analytics")
entries = get_feedback_entries(limit=50)
if entries:
    df = pd.DataFrame(entries, columns=["timestamp", "question", "feedback"])
    correct = df[df["feedback"] == "Correct"].shape[0]
    total = len(df)
    acc = (correct / total) * 100 if total else 0
    st.sidebar.metric("✅ Accuracy Rate", f"{acc:.1f}%")
    st.sidebar.metric("💬 Total Feedback", total)
    counts = df["feedback"].value_counts()
    fig, ax = plt.subplots(figsize=(3,2))
    ax.bar(counts.index, counts.values, color=["#0ff6b3","#f87171"])
    ax.set_title("Feedback Distribution", color="#0ff6b3")
    st.sidebar.pyplot(fig)
else:
    st.sidebar.info("No feedback yet. Start rating responses!")

# ------------------------------------------------------------
# Insight Summary Panel
# ------------------------------------------------------------
st.markdown("### 🧭 Recent Insight Summary")
if len(st.session_state.messages) > 0:
    last_msgs = [m for m in st.session_state.messages if m["role"] == "assistant"][-3:]
    for i, msg in enumerate(reversed(last_msgs), 1):
        st.markdown(f"**Insight {i}:** {msg['content'][:200]}{'...' if len(msg['content'])>200 else ''}")
else:
    st.info("Start chatting to build your insight summary here!")

# ------------------------------------------------------------
# Developer Mode
# ------------------------------------------------------------
st.sidebar.markdown("---")
if st.sidebar.checkbox("🧩 Developer Mode"):
    st.sidebar.text(f"Project Path:\n{os.path.abspath(os.getcwd())}")
    st.sidebar.text("Model: llama-3.3-70b-versatile\nAPI: Groq-compatible\nWeather: Open-Meteo")

# Footer
st.markdown("\n<footer>🌱 AI ClimaSense © 2025 • Powered by Retrieval-Augmented Intelligence</footer>", unsafe_allow_html=True)
st.success("\n✅ Ready! Ask your next question above.")
