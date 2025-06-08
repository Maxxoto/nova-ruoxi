# 🌌 Nova / 若曦 (*Ruòxī*, “Morning Star”)  
**Your Personal Agentic AI Second Brain**

Nova, also known as 若曦 (*Ruòxī*), is a bilingual, agentic AI assistant designed to help you think, learn, create, and grow. She’s not just a chatbot — she’s your cognitive partner, coding buddy, knowledge curator, and digital companion.

---

## ✨ Overview

Built on top of **[OpenWebUI](https://github.com/open-webui/open-webui)** and powered by **Qwen3-235B-A22B**, Nova features intelligent model routing, persistent memory, adaptive personas, and long-term personalization through her **Memory & Cognitive Profile (MCP)** system.

She understands both English and 中文 and adapts to a growing range of tasks — from deep reasoning to creative brainstorming.

---

## 🌟 Key Features

- 💬 Conversational AI with contextual and emotional awareness  
- 🧠 Personalized **Memory & Cognitive Profile (MCP)** *(Coming Soon)*  
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

| Role                     | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| 🌍 **Travel Planner**     | Builds itineraries and books tickets via external APIs                     |
| 💸 **Financial Advisor**  | Offers budgeting and investing advice via finetuned finance models         |
| 📥 **Inbox Summarizer**   | Summarizes emails or messages into concise digests                         |
| ⏳ **Task Manager Agent** | Organizes tasks and integrates with calendar tools                         |
| 📊 **Data Analyst**       | Parses CSVs, visualizes data, answers questions about datasets              |
| 🎭 **Persona Switcher**   | Adjusts tone and behavior based on user-defined roles                      |

---

## 🔀 Model Routing (via OpenRouter + Groq)

Nova routes tasks to different models depending on complexity and context:

| Task Type             | Primary Model                | Fallback / API Provider    |
|-----------------------|------------------------------|----------------------------|
| General reasoning     | Qwen3-235B-A22B (OpenRouter) | LLaMA 4 Maverick (Groq)    |
| Code generation       | DeepSeek Coder V3 0.352      | — (OpenRouter)             |
| Planning & reasoning  | DeepSeek R1                  | — (Groq)                   |
| Complex tasks         | Claude 4                     | — (OpenRouter)             |

> 🔌 Powered by **Groq** and **OpenRouter** for fast, reliable access to top-tier models.

---

## 🧠 Memory & Cognitive Profile (MCP) *(Coming Soon)*

Nova builds a persistent cognitive profile to deliver long-term personalization.

**Key Features**:
- Learns your preferences, tone, and goals over time  
- Remembers relevant facts and interaction history  
- Adapts behavior dynamically based on context  
- Stores data in structured formats + vector embeddings (JSON + ChromaDB)

---

## 🗃️ Tech Stack

| Component        | Technology / Service                              |
|------------------|---------------------------------------------------|
| UI Layer         | [OpenWebUI](https://github.com/open-webui/open-webui) |
| Core Model       | Qwen3-235B-A22B                                   |
| Routing Models   | DeepSeek R1 / Coder V3 / Claude 4 / LLaMA 4       |
| Embedding DB     | ChromaDB                                          |
| Backend API      | FastAPI *(for orchestration & plugin extensions)* |
| Voice / Audio    | Frontier TTS + diarization *(Planned)*            |
| STT & Vision     | Background speech-to-text + visual input *(Planned)* |

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
