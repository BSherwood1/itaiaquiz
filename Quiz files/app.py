import json
import streamlit as st

# --------------------------
# Load quiz questions
# --------------------------
@st.cache_data
def load_questions():
    with open("questions.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["questions"]

questions = load_questions()

# --------------------------
# Session State Initialization
# --------------------------
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "completed" not in st.session_state:
    st.session_state.completed = False

# --------------------------
# Header
# --------------------------
st.title("📘 AI Ethics & History Quiz")
st.caption("Answer the questions, view hints, and track your score!")

# --------------------------
# Quiz Logic
# --------------------------
if not st.session_state.completed:
    q = questions[st.session_state.q_index]

    st.subheader(f"Question {q['questionNumber']}")
    st.write(q["question"])

    # Show hint toggle
    with st.expander("💡 Need a hint?"):
        st.info(q["hint"])

    # Options
    options = [opt["text"] for opt in q["answerOptions"]]
    choice = st.radio("Choose your answer:", options, index=None)

    if st.button("Submit Answer", type="primary"):
        if choice is None:
            st.warning("Please select an option before submitting.")
        else:
            for opt in q["answerOptions"]:
                if opt["text"] == choice:
                    if opt["isCorrect"]:
                        st.success("✅ Correct!")
                        st.session_state.score += 1
                    else:
                        st.error("❌ Incorrect!")
                    st.info(f"Explanation: {opt['rationale']}")
            st.session_state.q_index += 1

            if st.session_state.q_index >= len(questions):
                st.session_state.completed = True

else:
    st.success("🎉 Quiz Completed!")
    st.write(f"Your Final Score: **{st.session_state.score} / {len(questions)}**")

    # Reset button
    if st.button("Restart Quiz"):
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.completed = False
