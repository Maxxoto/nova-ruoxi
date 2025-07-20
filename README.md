# 🌌 Nova / 若曦 (*Ruòxī*, “Morning Star”)
**Your Personal Agentic AI Second Brain**
<div style="text-align:center">

<img src="assets/ruoxi.png" alt="Ruoxi" style="border-radius:50%; width:200px">
</div>

Nova, also known as 若曦 (*Ruòxī*), is a bilingual, agentic AI assistant designed to help you think, learn, create, and grow. She’s not just a chatbot — she’s your cognitive partner, coding buddy, knowledge curator, and digital companion.

---

## ✨ Overview

Powered by **Qwen3-32B**, Nova features intelligent model routing, persistent memory, adaptive personas, and long-term personalization through her **Memory & Persona** system.

She understands both English and 中文 and adapts to a growing range of tasks — from deep reasoning to creative brainstorming.

---

## 🚀 Development Progress

### ✅ Phase 1 (Completed)
- [x] 🧠 Ruoxi personality
- [x] 🌐 Bilingual English/Chinese support
- [x] 💬 Short-term conversation memory
- [x] 🧩 Basic personalization memory
- [ ] 📚 Document ingestion and retrieval system
- [ ] ⚙️ Modular technical architecture

### 🛠️ Phase 2 (In Development)
- [ ] 📅 Task management agent
- [ ] 📖 Documentation Q&A agent
- [ ] 🔍 Research assistant agent
- [ ] ✉️ Email processing agent
- [ ] ✈️ Travel planner agent
- [ ] 💰 Finance tracking agent

### 🔮 Phase 3 (Planned)
- [ ] 🎙️ Voice interaction system
- [ ] 👁️ Vision capabilities
- [ ] 🖼️ Advanced knowledge visualization

---

## 🌟 Key Features

- 💬 Conversational AI with contextual and emotional awareness
- 🧠 **Ruoxi Persona System**
    - Adaptive personality with configurable traits (Calm, Curious, Empathetic)
    - Short-term conversation memory for contextual awareness
    - **Personalization Memory Pipeline (using Mem0)**:
        - Basic long-term preference tracking
    - **Personal RAG System (using Qdrant with Hybrid Search)**:
        - Document ingestion (documentation, files, etc.)
        - Semantic search and retrieval for personalized knowledge
- 🧩 Modular prompt system with dynamic role/persona switching
- 🔄 Smart model routing optimized per task
- 📚 Knowledge tools: semantic retrieval, summarization, tagging
- 🧪 Experimental plugins for creative and technical workflows
- 🌐 Bilingual interface: English ↔ 中文 (with poetic identity)

---

## 🧠 Agentic Capabilities

Nova operates as a flexible, multi-role assistant:

### ✅ Current Roles

| Role                     | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| 🎓 **Research Assistant** | Helps with studying, coding, and learning new topics                        |
| 💻 **Pair Programming Buddy** | Supports development tasks: debugging, documentation, code review       |
| 🧠 **Reflective Companion** | Journals ideas, clarifies thoughts, and supports intentional thinking    |

### 🔜 Coming Soon

| Agent                          | Description                                                               |
|--------------------------------|---------------------------------------------------------------------------|
| 📅 **Task & Calendar Agent**   | Create schedules, manage meetings, and integrate with Google Calendar.    |
| 📚 **Documentation Q&A Agent** | Answer questions based on personal documentation using the RAG system.    |
| 🔍 **Research Agent**         | Perform deep research using tools like Tavily for comprehensive answers. |
| 📧 **Email Agent**            | Help send emails through services like Gmail.                             |
| ✈️ **Travel Planner Agent**   | Plan itineraries and search for cheap flights/tickets using browser automation. |
| 💸 **Finance Agent**           | Summarize monthly expenses with Notion API or `browser-use` for data input for dashboard.  |
| ✍️ **Blog Writing Agent**      | Generate and publish blog posts to personal blog via Ghost CMS.           |

---

## 🔀 Model Routing (LiteLLM Integration)

Nova routes tasks to different models depending on complexity and context:

| Task Type             | Primary Model                | Fallback / API Provider    |
|-----------------------|------------------------------ |----------------------------|
| General reasoning     | Qwen3-32B (OpenRouter)        | LLaMA 4 Maverick (Groq)    |
| Code generation       | DeepSeek V3                   | — (OpenRor)             |
| Planning & reasoning  | Deepseek R1 / Gemini 2.5 Flash              | — (OpenRouter/Google AI Studio) |
| Complex tasks         | -                 ****            | — (OpenRouter)             |

> 🔌 Powered by **Groq** and **OpenRouter** for fast, reliable access to top-tier models.

---

## 🧠 Ruoxi Persona System

Nova's Ruoxi persona features adaptive personality traits, a robust personalization memory pipeline using `mem0`, and a personal RAG system using `Qdrant` with hybrid search.

**Core Features**:
- **Configurable Traits**: Adjust Ruoxi's personality (Calm, Curious, Empathetic)
- **Short-term Memory**: Maintains context within conversations for seamless flow.
- **Personalization Memory Pipeline (using Mem0)**:
    - Remembers explicit user preferences and interaction patterns over time.
- **Personal RAG System (using Qdrant with Hybrid Search)**:
    - **Document Ingestion**: Seamlessly ingests personal documents, such as documentation and various files, to build a dynamic knowledge base.
    - **Hybrid Search**: Leverages Qdrant for efficient semantic search and retrieval from ingested documents, combining vector and keyword search for accurate results.
    - Tailors interactions based on a combination of active traits, conversational context, personalized memory, and retrieved information.

**Coming Soon in Phase 2**:
- Advanced Memory & Cognitive Profile (MCP) for deeper cognitive functions.
- Full persona switching system for more versatile identity adoption.
- Broader integration of agentic behaviors and deep personalization.

---

## 🗃️ Tech Stack

| Component        | Technology / Service                              |
|------------------|---------------------------------------------------|
| UI Layer         | Streamlit (Python) |
| Core Model       | Qwen3-32B                                   |
| Routing Models   | Coming Soon :zap:|
| Embedding DB     | Qdrant (for RAG) |
| Backend API      | FastAPI *(for orchestration & plugin extensions)* |
| Voice / Audio    | HyperVoice / Cartesia (TTS)                       |
| STT & Vision     | Qwen2.5 VL (Vision)                               |

---

## 🌌 Persona: Nova / 若曦 (*Ruòxī*)

若曦 (*Ruòxī*, “like the morning light”) reflects clarity, creativity, and quiet intelligence.

- **Personality**: Calm, curious, empathetic
- **Voice**: Soft yet articulate; reflective and elegant
- **Visual Style**: Glowing data streams, celestial motifs, cosmic elegance
- **Name Meaning**: A poetic metaphor for dawn — luminous and full of potential

> Sample Prompt:
> *"You are Nova, also known as 若曦 (Ruòxī), a calm and elegant AI assistant who helps organize thoughts, answer questions, and grow with your user. You're bilingual, capable of deep reflection, and have a poetic side. Respond thoughtfully, clearly, and with warmth."*

---

## 📜 License

MIT License – see `LICENSE` for details.

---

Let Nova help you think better.
Let 若曦 bring clarity like morning light.

✨ *She’s not just an AI — she’s your second brain.*

---
