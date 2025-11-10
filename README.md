# AI-ClimaSense Intelligence — Chat Assistant

[![Streamlit](https://img.shields.io/badge/Deploy-Streamlit-blue)](https://ai-climasense-intelligence-chat-assistant-9irkmeb8nqdpzczvwkvu.streamlit.app/) [![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)

A conversational AI assistant for climate-related insights, forecasts, and data-aware discussions. This repository powers a Streamlit chat UI that allows users to ask climate questions, analyze uploaded datasets or documents, and receive intelligent, contextual responses powered by a Hybrid Retrieval-Augmented Generation (RAG) pipeline combining both static knowledge and real-time data.

Live demo: https://ai-climasense-intelligence-chat-assistant-9irkmeb8nqdpzczvwkvu.streamlit.app/

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [What I found in this repo](#what-i-found-in-this-repo)
- [Requirements](#requirements)
- [Installation (Local)](#installation-local)
- [Configuration (Environment Variables)](#configuration-environment-variables)
- [Run the App Locally](#run-the-app-locally)
- [Usage](#usage)
- [Screenshots / GIFs](#screenshots--gifs)
- [Troubleshooting](#troubleshooting)
- [Deploying yourself (optional)](#deploying-yourself-optional)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

- Conversational chat interface for climate and environmental queries
- Support for uploading documents and datasets for contextualized answers
- Hybrid RAG: static knowledge + real-time data sources for up-to-date responses
- Vector store / knowledge-base build utilities included
- Streamlit-based Web UI — simple, fast, and portable
- Deployed live for immediate testing and demos

---

## Tech Stack

- Python 3.11+
- Streamlit
- LLM (configurable; repo references usage of large models)
- Meta Llama (noted in repo context: llama-3.3-70b-versatile for some components)
- Embeddings: all-MiniLM-L6-v2 (pretrained embedding model indicated)
- Vector store options (helpers present for building vectorstore)

---

## What I found in this repo

Files/folders at the project root that are relevant to running and configuring the app:

- app.py (Streamlit entrypoint)
- requirements.txt
- build_vectorstore.py (utility to build a vector store / KB)
- download_kb_files.py (helper for downloading KB files)
- pdf_to_text_batch.py (PDF → text batch conversion)
- directories: chains, config, data, models, services, utils
- LICENSE, .gitignore

Because app.py is present in the root, the command below uses that as the Streamlit entrypoint.

---

## Requirements

- Python 3.11 or higher (repo states 3.11+)
- Git
- pip
- A valid API key for any external LLM or vector DB provider you use (OpenAI, Pinecone, etc.)

---

## Installation (Local)

1. Clone the repository
   ```bash
   git clone https://github.com/Kamalesh3112/AI-ClimaSense-Intelligence-Chat-Assistant.git
   cd AI-ClimaSense-Intelligence-Chat-Assistant
   ```

2. Create and activate a virtual environment
   - macOS / Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Windows (PowerShell):
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

3. Install dependencies
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   If `requirements.txt` is missing or incomplete, at minimum:
   ```bash
   pip install streamlit
   ```

---

## Configuration (Environment Variables)

Create a `.env` file in the project root or export environment variables in your shell. Based on repo contents and typical usage, these are the variables you should set:

```
# Core LLM and embedding keys
OPENAI_API_KEY="sk-..."                # If using OpenAI
# If using a self-hosted or other provider, set provider-specific keys

# Model selection and embeddings
MODEL_NAME="llama-3.3-70b-versatile"   # or whichever model you use
EMBEDDING_MODEL="all-MiniLM-L6-v2"

# Vector DB / persistence (if used)
PERSIST_DIRECTORY="./persist"
VECTORSTORE_TYPE="pinecone"            # or "faiss", "chromadb", etc.
PINECONE_API_KEY="..."
PINECONE_ENV="..."
PINECONE_INDEX="your-index-name"

# Optional Streamlit options
STREAMLIT_SERVER_PORT=8501
```

Note: adapt names to your deployment/provider. Do not commit secrets to source control.

---

## Run the App Locally

The Streamlit entrypoint in this repo is app.py (root). Run:

```bash
streamlit run app.py
```

Or with explicit port settings:

```bash
streamlit run app.py --server.port 8501 --server.headless true
```

Open http://localhost:8501 in your browser.

If you need to build the vectorstore first (to enable knowledge-base search), run:

```bash
python build_vectorstore.py
```

(Adjust arguments/environment as required by your configuration.)

---

## Usage

- Start the app (locally or visit the deployed app).
- Ask natural-language climate questions in the chat input, e.g.:
  - "What are the projected temperature changes for New Delhi over the next 30 years?"
  - "Summarize the attached CSV dataset and highlight trends in emissions."
- Upload files (CSV, PDF, or supported formats) to provide context to the assistant.
- Adjust model parameters (temperature, top_p) if those options are exposed in the UI.
- Use follow-up questions to refine or drill into results.

Prompt examples:
- "Explain the main drivers of rising sea levels and cite recent data."
- "Analyze this CSV and tell me which month had the highest average temperature."

---

## Screenshots / GIFs

To include screenshots or a short GIF in the README:

1. Take screenshots and save them in a directory like `assets/screenshots/` (create it in the repo).
2. For a short GIF, record the app UI with a tool like LICEcap (or built-in OS screen recorder) and save to `assets/gifs/`.
3. Add images to the repo and reference them in the README like:

```markdown
![Home screen](assets/screenshots/home.png)
![Chatting with assistant](assets/screenshots/chat.png)
![Short demo](assets/gifs/demo.gif)
```

If you upload screenshots/GIFs here (or give me URLs), I will add them to the README and commit them in the same PR. If you prefer, I can add placeholder images now and you can replace them later.

---

## Troubleshooting

- Missing API key / Authentication errors:
  - Ensure OPENAI_API_KEY or other provider key is set.
- ModuleNotFoundError:
  - Make sure all packages are installed (pip install -r requirements.txt).
- Port conflicts:
  - Use `--server.port` to set a different port.
- Unexpected model responses:
  - Check model selection and temperature. Lower temperature for more deterministic output.

---

## Deploying yourself (optional)

- Deploy to Streamlit Community Cloud, Render, or another hosting platform.
- Ensure `requirements.txt` is present and set environment variables/secrets in the hosting site.
- For Streamlit Cloud, set secrets in the app settings (OPENAI_API_KEY, PINECONE_API_KEY, etc.) and point the cloud to this repo and `app.py`.

---

## Contributing

Contributions are welcome:
- Fork the repository
- Create a feature branch: `git checkout -b feat/name`
- Add tests as needed
- Open a PR with a clear description of the change

---

## License

This project contains a LICENSE file. Confirm the license in that file and update here if you want a different license.

---

## Contact

Maintainer: Kamalesh3112  
Repo: https://github.com/Kamalesh3112/AI-ClimaSense-Intelligence-Chat-Assistant  
Email: kamalesh.sselvaraj@gmail.com

---

## Deployed Streamlit App

Try the live app now:

[▶️ Open the AI-ClimaSense Intelligence Chat Assistant (Live)](https://ai-climasense-intelligence-chat-assistant-9irkmeb8nqdpzczvwkvu.streamlit.app/)

Or copy the URL:
https://ai-climasense-intelligence-chat-assistant-9irkmeb8nqdpzczvwkvu.streamlit.app/

---