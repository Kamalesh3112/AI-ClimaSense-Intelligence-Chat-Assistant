# pdf_to_text_batch.py
"""
Batch converts all PDFs inside data/knowledge_base/ into clean text files.
Generates .txt versions for RAG embedding later.
"""

import os
import fitz  # PyMuPDF

# Folder path
kb_folder = "data/knowledge_base"

# Create folder if not exist
os.makedirs(kb_folder, exist_ok=True)

for filename in os.listdir(kb_folder):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(kb_folder, filename)
        txt_path = os.path.splitext(pdf_path)[0] + ".txt"

        print(f"Converting: {filename} -> {os.path.basename(txt_path)}")
        text = ""
        with fitz.open(pdf_path) as pdf:
            for page in pdf:
                text += page.get_text("text")

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)

print("\n✅ All PDF files converted to .txt successfully!")