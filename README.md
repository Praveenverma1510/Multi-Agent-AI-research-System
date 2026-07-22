# 🤖 Multi-Agent AI Research System

A **Multi-Agent AI Research System** built using **LangChain**, **Groq**, **Tavily Search API**, and **Streamlit**. The application automates the research process by coordinating multiple AI agents that search the web, analyze information, generate detailed reports, and review the final output for quality.

---

## 🎥 Project Demo

**Demo Video**

> https://drive.google.com/file/d/1m8qAeQIbtvnd-_d31p4h1dn-0G6BiWiK/view?usp=sharing

---

## 🚀 Features

* 🔎 AI-powered web research using Tavily Search API
* 🤖 Multi-agent architecture with specialized AI agents
* ⚡ High-speed LLM inference using Groq
* 📖 Intelligent information extraction and summarization
* 📝 Automated research report generation
* ✅ AI-based report review and feedback
* 🎨 Interactive Streamlit user interface
* 🔧 Modular and extensible codebase

---

## 🏗️ System Architecture

```text
                    User Research Topic
                            │
                            ▼
                  ┌──────────────────┐
                  │  Search Agent    │
                  │ (Tavily Search)  │
                  └──────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  Reader Agent    │
                  │ Analyze Results  │
                  └──────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  Writer Agent    │
                  │ Generate Report  │
                  └──────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  Critic Agent    │
                  │ Review & Improve │
                  └──────────────────┘
                            │
                            ▼
                 📄 Final Research Report
```

---

## 🤖 Agents

### 🔍 Search Agent

* Performs real-time web searches using the Tavily Search API.
* Collects relevant and reliable information.
* Retrieves recent search results.

### 📚 Reader Agent

* Reads and analyzes the search results.
* Extracts key insights and important facts.
* Organizes information for report generation.

### ✍️ Writer Agent

* Combines search results and extracted insights.
* Generates a structured research report.
* Produces clear and comprehensive content.

### 🧐 Critic Agent

* Reviews the generated report.
* Identifies missing information or inconsistencies.
* Provides suggestions to improve report quality.

---

## 🛠️ Tech Stack

* Python
* LangChain
* Groq
* Tavily Search API
* Streamlit
* BeautifulSoup
* Requests
* python-dotenv

---

## 📂 Project Structure

```text
Multi-Agent-AI-Research-System/
│
├── app.py                  # Streamlit UI
├── main.py                 # Entry point
├── pipeline.py             # Research workflow
├── agents.py               # AI agents
├── tools.py                # Search and scraping tools
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Praveenverma1510/Multi-Agent-AI-research-System.git

cd Multi-Agent-AI-research-System
```

Create a virtual environment.

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## ▶️ Running the Application

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## 📋 Application Workflow

1. Enter a research topic.
2. The Search Agent retrieves relevant web information using Tavily.
3. The Reader Agent analyzes and extracts important insights.
4. The Writer Agent generates a detailed research report.
5. The Critic Agent reviews the report and provides feedback.
6. The final research report is displayed in the Streamlit interface.

---

## 💡 Example Research Topics

* Artificial Intelligence in Healthcare
* Quantum Computing
* Renewable Energy
* Blockchain Technology
* Cybersecurity Trends
* Climate Change
* Large Language Models (LLMs)
* Edge AI
* Space Exploration
* Agentic AI

---

## 🌟 Future Improvements

* Export reports as PDF
* Automatic citations and references
* Research history
* Multi-language support
* Human-in-the-loop editing
* LangGraph workflow integration
* Vector database integration (RAG)
* Multi-model support (OpenAI, Anthropic, Gemini, etc.)
* Report comparison and versioning

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

* **Groq** for fast LLM inference.
* **Tavily Search API** for web search capabilities.
* **LangChain** for agent orchestration.
* **Streamlit** for the interactive user interface.

---

## 👨‍💻 Author

**Praveen Verma**

GitHub: https://github.com/Praveenverma1510

---

⭐ If you found this project useful, consider giving the repository a star!
