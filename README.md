# Medium Draft Improvement AI Agent (LangGraph)

![LangGraph Workflow](https://github.com/user-attachments/assets/e188c467-6a8a-49e4-8f1e-7d73747de34f)

An AI-powered editorial assistant built with LangGraph that analyzes, evaluates, revises, and explains improvements to Medium article drafts. The project demonstrates a stateful, multi-step AI agent workflow with conditional logic and LLM integration.

## 🚀 Project Overview

This project implements an AI agent workflow using LangGraph, a framework for building stateful, multi-node applications on top of large language models (LLMs). The agent simulates the behavior of a professional Medium editor by:

- **Analyzing** a draft article for writing issues
- **Evaluating** its quality for a target audience
- **Conditionally revising** the article if needed
- **Explaining** the editorial decisions made by the agent

A Streamlit web application is included to provide an interactive UI and visualize the LangGraph workflow.

## 🧠 Agent Workflow

The agent operates as a directed graph with conditional branching:

### 🔹 Nodes

| Node | Description |
|------|-------------|
| **analyze** | Identifies writing issues without rewriting |
| **evaluate** | Assigns a quality score (0–1) |
| **revise** | Improves clarity and flow if score is low |
| **explain** | Explains decisions and changes |

### 🔀 Control Flow

1. **If** `quality_score < 0.75` → article is revised
2. **Otherwise** → article is approved and explained

This introduces conditional branching, a key LangGraph feature.

## 🗂 State Definition

The agent uses a shared, evolving state defined with `TypedDict`:

```python
class MediumState(TypedDict):
    draft_text: str
    audience: str
    issues_found: List[str]
    quality_score: float
    final_text: str
    explanation: str
```

Each node reads from and updates this shared state.

## 🤖 LLM Integration

- **Model provider**: Groq
- **Model used**: LLaMA 3.1 (8B Instant)
- **LLM calls occur in**: Analysis, Evaluation, Revision
- **Environment variables**: Managed using `python-dotenv`

## 🖥 Streamlit Application

The Streamlit app allows users to:

- Paste a Medium article draft
- Select a target audience
- Run the LangGraph agent
- View:
  - Detected issues
  - Quality score
  - Revised article
  - Explanation of changes
- See a visual representation of the LangGraph workflow

## 📊 Graph Visualization

The LangGraph structure is exported as an image (`graph_visual.png`) using Mermaid syntax. This helps illustrate node transitions and conditional paths.

## 📁 Project Structure

```
Medium-Assistant-using-LangGraph-AI-Agent/
│
├── main.py               # LangGraph agent definition & execution
├── app.py                # Streamlit UI
├── graph_visual.png      # LangGraph workflow visualization
├── .env                  # API keys (not committed)
├── README.md             # Project documentation
└── requirements.txt      # Python dependencies
```

## ⚙️ Installation & Setup

### 1️⃣ Create virtual environment

```bash
python -m venv myenv
myenv\Scripts\activate
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

## ▶️ Running the Project

### Run the LangGraph agent (CLI)

```bash
python main.py
```

This will:
- Generate the graph visualization
- Execute the agent on a sample draft

### Run the Streamlit app

```bash
streamlit run app.py
```
