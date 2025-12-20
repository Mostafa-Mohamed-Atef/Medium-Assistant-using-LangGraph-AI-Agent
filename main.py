"""
Medium Draft Improvement AI Agent
--------------------------------
This agent analyzes a Medium article draft, evaluates its quality,
decides whether revision is needed, improves it if necessary,
and explains the editorial decisions.

Built with:
- LangGraph
- Gemini (Google Generative AI)
"""

from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv


# =========================================================
# 1. STATE DEFINITION
# =========================================================

class MediumState(TypedDict):
    draft_text: str
    audience: str
    issues_found: List[str]
    quality_score: float
    final_text: str
    explanation: str


# =========================================================
# 2. LLM SETUP (GEMINI)
# =========================================================
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0.4
)



# =========================================================
# 3. AGENT NODES
# =========================================================

def analysis_node(state: MediumState) -> MediumState:
    """
    Analyze the draft and detect writing issues.
    No rewriting is performed here.
    """
    prompt = f"""
You are a professional Medium editor.

Analyze the following draft and list writing issues only.
Do NOT rewrite the text.

Draft:
{state['draft_text']}

Return a bullet list of issues.
"""
    response = llm.invoke(prompt).content

    state["issues_found"] = [
        line.strip("- ").strip()
        for line in response.split("\n")
        if line.strip()
    ]
    return state


def evaluation_node(state: MediumState) -> MediumState:
    """
    Evaluate draft quality and assign a score between 0 and 1.
    """
    prompt = f"""
Evaluate the following Medium draft for:
- Clarity
- Structure
- Flow
- Audience suitability ({state['audience']})

Return ONLY a number between 0 and 1.

Draft:
{state['draft_text']}
"""
    response = llm.invoke(prompt).content.strip()

    try:
        state["quality_score"] = float(response)
    except ValueError:
        state["quality_score"] = 0.6  # safe fallback

    return state


def decision_node(state: MediumState) -> str:
    """
    Decide whether the article should be revised.
    """
    if state["quality_score"] < 0.75:
        return "revise"
    return "approve"


def revision_node(state: MediumState) -> MediumState:
    """
    Improve the draft while preserving the author's voice.
    """
    prompt = f"""
You are editing a Medium article.

Improve clarity, flow, and engagement.
Preserve the author's original voice and intent.
Fix only the detected issues.

Draft:
{state['draft_text']}

Detected issues:
{state['issues_found']}
"""
    response = llm.invoke(prompt).content
    state["final_text"] = response
    return state


def explanation_node(state: MediumState) -> MediumState:
    """
    Explain what the agent did and why.
    """
    if not state.get("final_text"):
        state["final_text"] = state["draft_text"]

    state["explanation"] = (
        f"The article was evaluated for a {state['audience']} audience and "
        f"received a quality score of {state['quality_score']:.2f}. "
        "Based on this evaluation, the agent decided whether revision was necessary. "
        "Any revisions focused on clarity, structure, and readability while "
        "preserving the original meaning and writing style."
    )
    return state


# =========================================================
# 4. BUILD LANGGRAPH
# =========================================================

builder = StateGraph(MediumState)

builder.add_node("analyze", analysis_node)
builder.add_node("evaluate", evaluation_node)
builder.add_node("revise", revision_node)
builder.add_node("explain", explanation_node)

builder.set_entry_point("analyze")

builder.add_edge("analyze", "evaluate")

builder.add_conditional_edges(
    "evaluate",
    decision_node,
    {
        "revise": "revise",
        "approve": "explain",
    }
)

builder.add_edge("revise", "explain")
builder.add_edge("explain", END)

agent = builder.compile()


# =========================================================
# 5. OPTIONAL: GRAPH VISUALIZATION (FOR REPORTS)
# =========================================================

# =========================================================
# 5. EXECUTION & VISUALIZATION
# =========================================================

if __name__ == "__main__":
    # Method A: Save as an Image file
    try:
        # This requires 'pyppeteer' or 'graphviz' - if they fail, use Method B
        with open("graph_visual.png", "wb") as f:
            f.write(agent.get_graph().draw_mermaid_png())
        print("Graph saved as 'graph_visual.png'")
    except Exception:
        print("\n--- Mermaid Code (Copy this to mermaid.live) ---")
        print(agent.get_graph().draw_mermaid())
        print("-----------------------------------------------\n")

    # Method B: Simple Console Execution
    inputs = {
        "draft_text": "AI is changing the world. It is very fast and cool.",
        "audience": "Tech enthusiasts"
    }

    print("Starting Agent...")
    for output in agent.stream(inputs):
        # This prints the name of the node that just finished
        for key, value in output.items():
            print(f"\n--- Node '{key}' finished ---")
