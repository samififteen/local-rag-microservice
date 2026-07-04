# 🚀 Enterprise RAG API

A high-performance RESTful microservice for **Retrieval-Augmented Generation (RAG)**. 

This API allows users to ingest private text documents, index them semantically using a local vector database, and query an LLM to get highly accurate, context-grounded answers without hallucinations. 

Built with **FastAPI**, **ChromaDB**, and **OpenAI**.

---

## ✨ Features
* **Document Ingestion (`/ingest`):** Automatically chunks raw text, generates OpenAI embeddings, and persists them locally via ChromaDB.
* **Context-Grounded Q&A (`/query`):** Performs cosine-similarity vector searches to find relevant facts and forces the LLM to answer *strictly* from the provided context.
* **Fully Typed:** Strict data validation using Pydantic.
* **Interactive UI:** Out-of-the-box Swagger UI documentation and testing environment.
* **100% Local Vector Storage:** No cloud database required; vectors are stored safely on your local disk.

---

## 🛠️ Tech Stack
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) + Uvicorn
* **Vector Database:** [ChromaDB](https://www.trychroma.com/)
* **AI Ecosystem:** OpenAI API (Embeddings & GPT-4o-mini)
* **Data Validation:** Pydantic

---

## 📂 Project Structure

\`\`\`text
fastapi_rag/
├── app/
│   ├── __init__.py
│   ├── main.py            # API routes and configuration
│   ├── schemas.py         # Pydantic input/output validation models
│   └── services/
│       ├── __init__.py
│       ├── vector_store.py# Text chunking and ChromaDB operations
│       └── llm.py         # Prompt engineering and OpenAI inference
├── chroma_db_data/        # Auto-generated local vector storage
├── .env                   # Environment variables (API Keys)
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
\`\`\`

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.10+
* An [OpenAI API Key](https://platform.openai.com/)

### 2. Installation
Clone the repository and navigate into the project directory:
\`\`\`bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
\`\`\`

Create a virtual environment and activate it:
\`\`\`bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
\`\`\`

Install the required dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`
*(Note: This project strictly pins `numpy<2.0.0` and `httpx<0.28.0` to ensure ChromaDB and OpenAI client compatibility).*

### 3. Environment Variables
Create a `.env` file in the root directory and add your OpenAI API key:
\`\`\`env
OPENAI_API_KEY=sk-your_actual_api_key_here
\`\`\`

### 4. Run the Server
Launch the FastAPI application using Uvicorn:
\`\`\`bash
uvicorn app.main:app --reload
\`\`\`

---

## 📖 API Usage

Once the server is running, navigate to **http://127.0.0.1:8000/docs** in your browser to access the interactive Swagger UI.

### 1. Ingest Data (`POST /ingest`)
Feed your AI private knowledge.
**Payload:**
\`\`\`json
{
  "text": "Project Aetheris is a confidential energy initiative launched in 2025. It uses deep-sea geothermal vents to generate clean electrical grid power. The lead scientist is Dr. Helena Vance.",
  "source_name": "aetheris_briefing.txt"
}
\`\`\`

### 2. Query Data (`POST /query`)
Ask questions based on your ingested knowledge.
**Payload:**
\`\`\`json
{
  "question": "Who is the lead scientist of Project Aetheris?",
  "top_k": 3
}
\`\`\`

**Response:**
\`\`\`json
{
  "question": "Who is the lead scientist of Project Aetheris?",
  "answer": "The lead scientist of Project Aetheris is Dr. Helena Vance.",
  "sources_used": [
    "Project Aetheris is a confidential energy initiative launched in 2025... The lead scientist is Dr. Helena Vance."
  ]
}
\`\`\`

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME/issues).
