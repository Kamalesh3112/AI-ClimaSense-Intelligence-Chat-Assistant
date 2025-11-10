import os
import time
from utils.data_utils import build_vectorstore_from_local_docs

def auto_rebuild_vectorstore(kb_dir="data/knowledge_base", vs_dir="data/vectorstore"):
    timestamp_file = os.path.join(vs_dir, ".timestamp")

    # Get last recorded timestamp (if any)
    last_build_time = 0
    if os.path.exists(timestamp_file):
        with open(timestamp_file, "r") as f:
            last_build_time = float(f.read().strip())

    # Get newest modification time in knowledge base
    newest_doc_time = max(
        os.path.getmtime(os.path.join(kb_dir, f))
        for f in os.listdir(kb_dir)
        if f.endswith((".pdf", ".txt"))
    )

    # Rebuild only if needed
    if newest_doc_time > last_build_time:
        print("🔄 Detected updated knowledge base files. Rebuilding vectorstore...")
        build_vectorstore_from_local_docs()

        # Update timestamp
        with open(timestamp_file, "w") as f:
            f.write(str(time.time()))
        print("✅ Vectorstore refreshed and timestamp updated.")
    else:
        print("✅ Vectorstore is already up to date.")