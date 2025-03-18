import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Function Definitions ---
def generate_math_study_plan(grade_level, weak_topics, available_hours):
    """Generates a personalized 7-day math study plan."""
    prompt = f"""
    Create a personalized 7-day math study plan for a student.
    Grade Level: {grade_level}
    Weak Topics: {weak_topics}
    Available Study Hours per Day: {available_hours}
    Focus on step-by-step explanations and adaptive practice.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an expert math tutor."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except openai.AuthenticationError as e:
        st.error(f"OpenAI Authentication Error: {e}")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def generate_adaptive_questions(topic, difficulty, previous_mistakes):
    """Generates 5 adaptive math practice questions."""
    prompt = f"Generate 5 {difficulty}-level math problems on {topic}. Consider previous mistakes: {previous_mistakes}. Provide hints if needed."
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a helpful math tutor."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except openai.AuthenticationError as e:
        st.error(f"OpenAI Authentication Error: {e}")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def explain_math_concept(topic, student_mistakes):
    """Explains a math concept in simple terms."""
    prompt = f"Explain {topic} in simple terms with examples. Address these common mistakes: {student_mistakes}. Provide real-world applications."
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a knowledgeable math tutor."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except openai.AuthenticationError as e:
        st.error(f"OpenAI Authentication Error: {e}")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def reinforce_concept_with_resources(topic, mistake_count):
    """Suggests additional learning resources."""
    try:
        if mistake_count > 2:
            prompt = f"Suggest interactive videos, real-world applications, and gamified exercises to help a student understand {topic} better."
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You are an expert math tutor providing engaging resources."},
                          {"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        else:
            return "Keep practicing! If you struggle again, I will suggest additional resources."
    except openai.AuthenticationError as e:
        st.error(f"OpenAI Authentication Error: {e}")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# --- Streamlit UI ---
st.set_page_config(page_title="Math Study Planner", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .big-font { font-size: 30px !important; font-weight: bold; }
    .stTextInput > div > div > input { border: 2px solid #4CAF50; border-radius: 5px; padding: 10px; }
    .stNumberInput > div > div > input { border: 2px solid #4CAF50; border-radius: 5px; padding: 10px; }
    .stSelectbox > div > div > div { border: 2px solid #4CAF50; border-radius: 5px; padding: 10px; }
    .stButton > button { background-color: #4CAF50; color: white; padding: 14px 20px; border: none; border-radius: 5px; cursor: pointer; }
    .stButton > button:hover { background-color: #3e8e41; }
    .stTextArea > div > div > textarea { border: 2px solid #4CAF50; border-radius: 5px; padding: 10px; }
    .st-expander { border: 1px solid #4CAF50; border-radius: 5px; padding: 10px; margin-bottom: 10px; }
    .centered-header { text-align: center; color: #4CAF50; }
    .input-section { margin-bottom: 20px; }
    .output-section { margin-top: 20px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 class='centered-header'>Math Study Planner</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<h2 class='big-font'>Generate Study Plan</h2>", unsafe_allow_html=True)
    with st.container(border=True):
        grade_level = st.number_input("Enter your grade level:", min_value=1, step=1)
        weak_topics = st.text_input("Enter weak math topics (comma-separated):")
        available_hours = st.number_input("Enter available study hours per day:", min_value=1, step=1)

        if st.button("Generate Study Plan"):
            if grade_level and weak_topics and available_hours:
                study_plan = generate_math_study_plan(grade_level, weak_topics, available_hours)
                if study_plan:
                    st.markdown("<h3 class='centered-header'>Study Plan:</h3>", unsafe_allow_html=True)
                    st.write(study_plan)
            else:
                st.warning("Please fill in all fields.")

    st.markdown("<h2 class='big-font'>Adaptive Practice Questions</h2>", unsafe_allow_html=True)
    with st.container(border=True):
        topic = st.text_input("Enter a math topic for practice questions:")
        difficulty = st.selectbox("Select difficulty level:", ["easy", "medium", "hard"])
        previous_mistakes = st.text_input("List common mistakes you've made (comma-separated):")

        if st.button("Generate Questions"):
            if topic and difficulty and previous_mistakes:
                questions = generate_adaptive_questions(topic, difficulty, previous_mistakes)
                if questions:
                    st.markdown("<h3 class='centered-header'>Practice Questions:</h3>", unsafe_allow_html=True)
                    st.write(questions)
            else:
                st.warning("Please fill in all fields.")

with col2:
    st.markdown("<h2 class='big-font'>Concept Explanation</h2>", unsafe_allow_html=True)
    with st.container(border=True):
        concept_topic = st.text_input("Enter a math topic for explanation:")
        concept_mistakes = st.text_input("List common mistakes (comma-separated):")

        if st.button("Explain Concept"):
            if concept_topic and concept_mistakes:
                explanation = explain_math_concept(concept_topic, concept_mistakes)
                if explanation:
                    st.markdown("<h3 class='centered-header'>Concept Explanation:</h3>", unsafe_allow_html=True)
                    st.write(explanation)
            else:
                st.warning("Please fill in all fields.")

    st.markdown("<h2 class='big-font'>Additional Learning Resources</h2>", unsafe_allow_html=True)
    with st.container(border=True):
        resource_topic = st.text_input("Enter a math topic")