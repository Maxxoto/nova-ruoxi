# 🧠 若曩 General Toolset Overview

This document outlines the **core tool modules** for 若曩 Ruòxī — your agentic second brain. These tools serve as foundational cognitive skills across memory, web access, document analysis, vision, and communication.

---

## ✅ Current Tools

| Tool Name           | Description                                                     |
| ------------------- | --------------------------------------------------------------- |
| `followup_question` | Generates follow-up questions to clarify or deepen conversation |
| `summarize_chat`    | Summarizes previous chat turns into concise context             |

---

## 🔧 Suggested Core Tools (Phase 1–2)

### 🧠 Memory Tools

| Tool Name        | Purpose                                                  |
| ---------------- | -------------------------------------------------------- |
| `memory_store`   | Save meaningful content to memory (Qdrant or PostgreSQL) |
| `memory_recall`  | Retrieve relevant memory based on current query          |
| `summarize_chat` | Condense chat turns for context and logging              |

---

### 🌐 Knowledge & Search Tools

| Tool Name            | Purpose                                         |
| -------------------- | ----------------------------------------------- |
| `search_web`         | Search the web using Google/DuckDuckGo/Bing API |
| `rag_query`          | Ask questions based on embedded documents       |
| `summarize_document` | Generate summaries from file or URL content     |

---

### 📚 Document Understanding Tools

| Tool Name            | Purpose                                             |
| -------------------- | --------------------------------------------------- |
| `extract_entities`   | Pull key entities (people, actions, data) from text |
| `note_task`          | Extract and store tasks/thoughts as notes           |
| `summarize_document` | Summarize uploaded PDFs, HTML, Markdown, etc.       |

---

### 👁️ Perception & Multimodal Tools

| Tool Name              | Purpose                                 |
| ---------------------- | --------------------------------------- |
| `describe_image`       | Analyze and describe uploaded images    |
| `describe_video_frame` | Capture and describe video/screen frame |

---

### 🎨 Language & Expression Tools

| Tool Name           | Purpose                                             |
| ------------------- | --------------------------------------------------- |
| `rephrase_for_tone` | Rewrite text in 若曩's style (poetic, gentle, etc.) |
| `followup_question` | Generate follow-up question (already added)         |

---

## 🪄 Tool Implementation Order

1. ✅ `followup_question`
2. ✅ `summarize_chat`
3. 🔍 `search_web`
4. 🧠 `memory_store` + `memory_recall`
5. 📄 `summarize_document`
6. 📷 `describe_image`
7. ↺ `rephrase_for_tone`

---

## 📦 Tool Template (LangChain)

```python
from langchain_core.tools import tool

@tool
def rephrase_for_tone(text: str, tone: str = "poetic") -> str:
    """Rewrites input text to match the specified tone (e.g., poetic, gentle)."""
    prompt = f"Rewrite the following in a {tone} tone:\n{text}"
    return llm.invoke(prompt)
```

---

## 🌸 Example Tool Registry

```python
from my_tools import (
    followup_question,
    summarize_chat,
    search_web,
    summarize_document,
    memory_store,
    memory_recall,
    describe_image,
    rephrase_for_tone
)

tools = [
    followup_question,
    summarize_chat,
    search_web,
    summarize_document,
    memory_store,
    memory_recall,
    describe_image,
    rephrase_for_tone
]
```

---
