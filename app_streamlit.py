import streamlit as st

import openai

import os

from dotenv import load_dotenv



# Load environment variables from .env file

load_dotenv(override=True)


# This will print to your Streamlit Cloud logs

print(f"Before API Key assignment: openai.api_key is: {openai.api_key}")

openai.api_key = os.getenv("OPENAI_API_KEY")

print(f"After API Key assignment: openai.api_key is: {openai.api_key}")



# --- Function Definitions ---

def generate_math_study_plan(grade_level, weak_topics, available_hours):
    """Generates a personalized 7-day math study plan.""" #corrected line.
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

        return None  # Indicate failure

    except Exception as e:

        st.error(f"An error occurred: {e}")

        return None  # Indicate failure



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

st.title("Math Study Planner")



# Study Plan Generator

st.header("Generate Study Plan")

grade_level = st.number_input("Enter your grade level (e.g., 6, 7, 8):", min_value=1, step=1)

weak_topics = st.text_input("Enter weak math topics (comma-separated):")

available_hours = st.number_input("Enter available study hours per day:", min_value=1, step=1)



if st.button("Generate Study Plan"):

    if grade_level and weak_topics and available_hours:

        study_plan = generate_math_study_plan(grade_level, weak_topics, available_hours)

        if study_plan:  # Only display if plan was generated

            st.subheader("Study Plan:")

            st.write(study_plan)

    else:

        st.warning("Please fill in all fields.")



# Adaptive Questions Generator

st.header("Adaptive Practice Questions")

topic = st.text_input("Enter a math topic for practice questions:")

difficulty = st.selectbox("Select difficulty level:", ["easy", "medium", "hard"])

previous_mistakes = st.text_input("List common mistakes you've made (comma-separated):")



if st.button("Generate Questions"):

    if topic and difficulty and previous_mistakes:

        questions = generate_adaptive_questions(topic, difficulty, previous_mistakes)

        if questions: # Only display if questions were generated

            st.subheader("Practice Questions:")

            st.write(questions)

    else:

        st.warning("Please fill in all fields.")



# Concept Explanation

st.header("Concept Explanation")

concept_topic = st.text_input("Enter a math topic for explanation:")

concept_mistakes = st.text_input("List common mistakes (comma-separated):")



if st.button("Explain Concept"):

    if concept_topic and concept_mistakes:

        explanation = explain_math_concept(concept_topic, concept_mistakes)

        if explanation: # Only display if explanation was generated

            st.subheader("Concept Explanation:")

            st.write(explanation)

    else:

        st.warning("Please fill in all fields.")



# Reinforce with Resources

st.header("Additional Learning Resources")

resource_topic = st.text_input("Enter a math topic:")

mistake_count = st.number_input("How many times have you struggled with this topic?", min_value=0, step=1)



if st.button("Get Resources"):

    if resource_topic is not None:

        resources = reinforce_concept_with_resources(resource_topic, mistake_count)

        if resources: # Only display if resources were generated

            st.subheader("Resources:")

            st.write(resources)

    else:

        st.warning("Please enter a topic.")