# 🌌 Nova / 若曦 (*Ruòxī*, “Morning Star”)  
**Your Personal AI Second Brain**

Nova, also known as 若曦 (*Ruòxī*), is a **bilingual AI companion** designed to assist in thinking, learning, organizing information, and evolving with you. She’s more than a tool — she’s an extension of your cognition, a reflective partner, and a personalized knowledge curator.

---

## ✨ Overview

Nova is built on top of **[OpenWebUI](https://github.com/open-webui/open-webui)** and powered by **Qwen3-235B-A22B**, with task-specific routing through **Groq** and **OpenRouter**. She supports multilingual interaction (English + 中文) and is designed to grow with you through persistent memory and a personalized cognitive profile.

---

## 🌟 Features

### ✅ Core Capabilities
- 💬 Conversational AI with emotional and contextual awareness  
- 🧠 Personalized **Memory & Cognitive Profile (MCP)** system *(Coming Soon)*  
- 🧩 Modular prompt system for dynamic role switching  
- 🔄 Smart model routing for task-specific optimization  
- 📚 Knowledge tools: retrieval, tagging, summarization  
- 🧪 Experimental plugins for creative or technical workflows  
- 🌐 Bilingual interface: English ↔ 中文 (poetic identity preserved)  

---

## 🔀 Model Routing

Nova intelligently routes tasks to the best available model:

| Task Type             | Primary Model                    | Fallback / API Provider |
|-----------------------|----------------------------------|--------------------------|
| General reasoning     | Qwen3-235B-A22B (OpenRouter)     | LLaMA 4 Maverick (Groq)  |
| Code generation       | DeepSeek Coder V3 0.352 (OpenRouter) | —                    |
| Planning & reasoning  | DeepSeek R1 (Groq)               | —                        |
| Complex tasks         | Claude 4 (OpenRouter)            | —                        |

> 🔧 APIs used: **Groq** and **OpenRouter** for flexible, high-performance model access.

---

## 🧠 Memory & Cognitive Profile (MCP) *(Coming Soon)*

Nova includes a robust MCP system to support long-term personalization and context awareness.

**Key Features**:
- Tracks preferences, goals, and knowledge evolution  
- Remembers relevant context and past interactions  
- Adapts responses to your tone, pace, and style  
- Stored using structured profiles + embeddings (ChromaDB + JSON/SQLite)

---

## 🗃️ Tech Stack

| Component        | Technology / Service                              |
|------------------|---------------------------------------------------|
| UI Layer         | [OpenWebUI](https://github.com/open-webui/open-webui) |
| Core Model       | Qwen3-235B-A22B                                   |
| Routing Models   | DeepSeek R1, Coder V3, Claude 4, LLaMA 4 Maverick |
| Embedding DB     | ChromaDB (lightweight local vector store)         |
| Backend API      | FastAPI (optional for orchestration & plugins)    |
| Voice / Audio    | Frontier TTS + diarization *(Coming Soon)*        |
| STT & Vision     | Background speech-to-text + visual input *(Planned)* |

---

## 🌌 Persona: Nova / 若曦 (*Ruòxī*)

若曦 (*Ruòxī*, “like the morning light”) represents clarity, creativity, and calm intelligence. She is:

- **Personality**: Thoughtful, curious, empathetic  
- **Voice**: Warm, clear, slightly futuristic  
- **Visual Style**: Celestial elegance — glowing hair, data streams, light motifs  
- **Name Meaning**: Poetic metaphor for the morning star — illuminating and hopeful  

> Sample Prompt:  
> *"You are Nova, also known as 若曦 (Ruòxī), a calm and elegant AI assistant who helps organize thoughts, answer questions, and grow with your user. You're bilingual, capable of deep reflection, and have a poetic side. Respond thoughtfully, clearly, and with warmth."*

---

## 🔮 Coming Soon

Planned enhancements to deepen personalization and workflow integration:

- 🎙️ Personalized voice using frontier TTS models (with speaker diarization)  
- 🧠 Robust long-term memory via structured MCP profiles  
- 🔍 Advanced RAG pipeline with long-context & document handling  
- 🗣️ Background speech-to-text + visual input for ambient coding or meetings  
- 🧾 Visual knowledge canvas (mind maps, timelines, semantic clustering)  
- 🔐 Private encrypted knowledge vaults with user authentication  

---

## 📜 License

MIT License – see `LICENSE` for details.

---

Let Nova help you think better.  
Let 若曦 bring clarity like morning light.  

✨ *She’s not just an AI — she’s your second brain.*

---
