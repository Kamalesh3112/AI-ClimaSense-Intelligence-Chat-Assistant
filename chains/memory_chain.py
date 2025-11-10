"""
Memory helper to be used by the app to maintain short-term conversation state.
"""
from langchain.memory import ConversationBufferMemory

def get_memory():
    return ConversationBufferMemory(memory_key="chat_history", return_messages=True)