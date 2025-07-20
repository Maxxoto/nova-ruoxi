## 🗺️ Feature Roadmap

Nova / 若曦 is evolving steadily toward becoming a deeply personalized, agentic second brain. Below is a categorized roadmap outlining current progress and future features.

---

### ✅ Phase 1: Core Ruoxi Persona Foundation (In Progress)
**Conversational Core**

    - Dynamic role prompting with Ruoxi personality \
    - Bilingual support (English + 中文)

**Ruoxi Persona System**

    - Configurable personality traits (Calm, Curious, Empathetic)
    - Short-term conversation memory

**Personalization Memory Pipeline (using Mem0)**:

    - Basic long-term preference tracking
    - Adaptive responses based on traits and memory

**Personal RAG System (using Qdrant with Hybrid Search)**

    - Document ingestion (documentation, files, etc.)
    - Process: Ingest & Chunk -> Embed -> Hybrid Search with Qdrant
    - Simple retrieval for personalized knowledge

**Technical Foundation**

    - Embedding storage using Qdrant (for RAG data)
    - Optional FastAPI backend
    - Modular architecture for future expansion

### 🔜 Phase 2:Agentic Behavior & Specialized Agents

This phase introduces specialized agents capable of performing concrete tasks and further enhances personalization. These agents will leverage the core Ruoxi Persona System (traits, memory, RAG) developed in Phase 1.

**Agentic Capabilities**

*   **Task Management & Calendar Agent**
    *   Create and manage schedules, meetings, and time blocks.
    *   Integrate with Google Calendar for syncing and event creation.
*   **Documentation Q&A Agent**
    *   Leverage the Personal RAG system (from Phase 1) to answer questions based on personal documentation.
*   **Research Agent**
    *   Perform deep research using tools like Tavily.
    *   Synthesize information for intelligent responses.
*   **Email Agent**
    *   Summarize emails and messages.
    *   Compose and send emails through services like Gmail.
*   **Travel Planner Agent**
    *   Generate itineraries based on user preferences.
    *   Search for cheap flights/tickets using external libraries (e.g., `browser-use.com` or UI Tars).
    *   Create reminders and packing lists.
*   **Finance Agent**
    *   Summarize monthly expenses.
    *   Integrate with Notion API or leverage `browser-use` for data input for dashboard.
*   **Blog Writing Agent**
    *   Generate and publish blog posts to personal blog.
    *   Integrate with Ghost CMS via API.


---

### 🧪 Phase 3: Multimodal & Voice Interactions

**Vision Capabilities**
- Tool detection: If base model lacks vision, route to vision tools using Qwen2.5 VL.

**Voice Mode**
- **Core Voice Functionality (TTS + STT)**:
    - Text-to-Speech (TTS) for personalized voice generation (using HyperVoice or Cartesia).
    - Speech-to-Text (STT) for accurate transcription.
- **Voice Mode UI**:
    - Dedicated user interface for voice interactions.
- **Background Voice Functionality**:
    - Passive listening mode for meeting transcription.
    - Real-time feedback during pair programming sessions.

**Visual Knowledge Canvas** *(Planned)*
- Mind maps, timelines, concept graphs from memory

---

### 💼 Phase 4: Specialized Agents / Domains

💸 **Financial Planner Agent**
- Budgeting, expense tracking, and investment suggestions
- Expense detection using email for receipt , credit card, and bank statement parsing


💰 **Financial Advisor Agent (Advanced)**
- Expense and investment suggestions
- Finetuned open-source finance models or RAG-based tooling (optional)

🌍 **Travel Planner Agent**
- Generate itineraries based on user personalities
- Find cheap flights, hotels, and activities based on most recent travel history and popular apps in user's region
- Create reminders for travel dates and times
- Create a packing list based on user's travel history and preferences


🔌 **Tool Use & Plugin API** *(Planned)*
- Let Nova interact with external APIs, shell commands, or apps via agent tools

🔐 **Encrypted Knowledge Vaults** *(Planned)*
- Private data stores bound to user profiles with optional auth

---

## 📌 Long-Term Vision

Nova will evolve into a modular, multimodal cognitive framework that mirrors your thinking, adapts to your goals, and acts as a lifelong learning companion — across domains, devices, and languages.

---
