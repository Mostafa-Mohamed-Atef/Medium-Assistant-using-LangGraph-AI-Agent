import streamlit as st
from PIL import Image
from main import agent  # import your compiled LangGraph agent

st.set_page_config(page_title="Medium Draft Improvement Agent", layout="wide")

st.title("✍️ Medium Draft Improvement AI Agent")
st.markdown(
    "This app uses **LangGraph** to analyze, evaluate, revise, and explain improvements "
    "to a Medium article draft."
)

# ===============================
# Sidebar – Graph Visualization
# ===============================
st.sidebar.header("📊 Agent Graph")

try:
    img = Image.open("graph_visual.png")
    st.sidebar.image(img, caption="LangGraph Workflow", width="stretch")
except FileNotFoundError:
    st.sidebar.warning("Graph image not found. Run main.py once to generate it.")

# ===============================
# User Inputs
# ===============================
st.subheader("📝 Draft Input")

draft_text = st.text_area(
    "Paste your Medium draft here:",
    height=200,
    placeholder="Write your article draft..."
)

audience = st.selectbox(
    "Target Audience",
    ["Tech enthusiasts", "Beginners", "Startup founders", "General readers"]
)

run_button = st.button("🚀 Improve Draft")

# ===============================
# Run Agent
# ===============================
if run_button and draft_text.strip():
    with st.spinner("Running AI agent..."):
        inputs = {
            "draft_text": draft_text,
            "audience": audience
        }

        final_state = {}
        for step in agent.stream(inputs):
            for _, value in step.items():
                final_state.update(value)

    # ===============================
    # Outputs
    # ===============================
    st.success("Agent completed successfully!")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔍 Issues Found")
        st.write(final_state.get("issues_found", []))

        st.subheader("📈 Quality Score")
        st.metric("Score", f"{final_state.get('quality_score', 0):.2f}")

    with col2:
        st.subheader("✏️ Final Article")
        st.write(final_state.get("final_text", draft_text))

    st.subheader("🧠 Explanation")
    st.write(final_state.get("explanation"))

elif run_button:
    st.warning("Please enter a draft article.")
