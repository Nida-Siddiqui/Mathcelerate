from flask import Flask, request, jsonify, send_from_directory
import openai
import os
from dotenv import load_dotenv
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__, static_folder='static')

def generate_math_study_plan(grade_level, weak_topics, available_hours):
    """Generates a personalized math study plan using the OpenAI API."""
    prompt = f"""
    Create a personalized 7-day math study plan for a middle school student.
    Grade Level: {grade_level}
    Weak Topics: {weak_topics}
    Available Study Hours per Day: {available_hours}
    Focus on step-by-step explanations and adaptive practice.
    """
    try:
        logging.info(f"Generating study plan with: {grade_level=}, {weak_topics=}, {available_hours=}")
        print(f"Generating study plan with: {grade_level=}, {weak_topics=}, {available_hours=}")  # Debugging print
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an expert math tutor."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating study plan: {e}")
        print(f"Error generating study plan: {e}")  # Debugging print
        return None  # Or raise the exception if you want it to propagate

def generate_adaptive_questions(topic, difficulty, previous_mistakes):
    """Generates adaptive math questions using the OpenAI API."""
    prompt = f"Generate 5 {difficulty}-level math problems on {topic}. Consider previous mistakes: {previous_mistakes}. Provide hints if needed."
    try:
        logging.info(f"Generating questions with: {topic=}, {difficulty=}, {previous_mistakes=}")
        print(f"Generating questions with: {topic=}, {difficulty=}, {previous_mistakes=}")  # Debugging print
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a helpful math tutor."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating questions: {e}")
        print(f"Error generating questions: {e}")  # Debugging print
        return None

def explain_math_concept(topic, student_mistakes):
    """Explains a math concept using the OpenAI API."""
    prompt = f"Explain {topic} in simple terms with examples. Address these common mistakes: {student_mistakes}. Provide real-world applications."
    try:
        logging.info(f"Explaining concept with: {topic=}, {student_mistakes=}")
        print(f"Explaining concept with: {topic=}, {student_mistakes=}")  # Debugging print
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a knowledgeable math tutor."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error explaining concept: {e}")
        print(f"Error explaining concept: {e}")  # Debugging print
        return None

def reinforce_concept_with_resources(topic, mistake_count):
    """Suggests resources to reinforce a math concept using the OpenAI API."""
    if mistake_count > 2:
        prompt = f"Suggest interactive videos, real-world applications, and gamified exercises to help a middle school student understand {topic} better."
        try:
            logging.info(f"Reinforcing resources with: {topic=}, {mistake_count=}")
            print(f"Reinforcing resources with: {topic=}, {mistake_count=}")  # Debugging print
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You are an expert math tutor providing engaging resources."},
                          {"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error reinforcing resources: {e}")
            print(f"Error reinforcing resources: {e}")  # Debugging print
            return None
    else:
        return "Keep practicing! If you struggle again, I will suggest additional resources."

@app.route('/')
def index():
    """Serves the index.html file."""
    return send_from_directory('static', 'index.html')

@app.route('/generate_study_plan', methods=['POST'])
def generate_study_plan_api():
    """API endpoint to generate a study plan."""
    try:
        data = request.get_json()
        logging.info(f"Received data for study plan: {data}")
        print("Received data for study plan:", data)  # Debugging print

        # Input Validation (Example)
        if not data or not all(key in data for key in ('grade_level', 'weak_topics', 'available_hours')):
            return jsonify({'error': 'Missing required fields'}), 400

        grade_level = data.get('grade_level')  # Use .get() for safer access
        weak_topics = data.get('weak_topics')
        available_hours = data.get('available_hours')

        result = generate_math_study_plan(grade_level, weak_topics, available_hours)

        if result:
            logging.info(f"Generated study plan: {result}")
            print("Generated study plan:", result)  # Debugging print
            return jsonify({'result': result})
        else:
            return jsonify({'error': 'Failed to generate study plan'}), 500

    except Exception as e:
        logging.exception("Error processing study plan request")
        return jsonify({'error': str(e)}), 500

@app.route('/generate_questions', methods=['POST'])
def generate_questions_api():
    """API endpoint to generate adaptive questions."""
    try:
        data = request.get_json()
        logging.info(f"Received data for questions: {data}")
        print("Received data for questions:", data)  # Debugging print

        if not data or not all(key in data for key in ('topic', 'difficulty', 'previous_mistakes')):
            return jsonify({'error': 'Missing required fields'}), 400

        topic = data.get('topic')
        difficulty = data.get('difficulty')
        previous_mistakes = data.get('previous_mistakes')
        result = generate_adaptive_questions(topic, difficulty, previous_mistakes)

        if result:
            logging.info(f"Generated questions: {result}")
            print("Generated questions:", result)  # Debugging print
            return jsonify({'result': result})
        else:
            return jsonify({'error': 'Failed to generate questions'}), 500

    except Exception as e:
        logging.exception("Error processing questions request")
        return jsonify({'error': str(e)}), 500

@app.route('/explain_concept', methods=['POST'])
def explain_concept_api():
    """API endpoint to explain a math concept."""
    try:
        data = request.get_json()
        logging.info(f"Received data for concept explanation: {data}")
        print("Received data for concept explanation:", data)  # Debugging print

        if not data or not all(key in data for key in ('topic', 'student_mistakes')):
            return jsonify({'error': 'Missing required fields'}), 400

        topic = data.get('topic')
        student_mistakes = data.get('student_mistakes')
        result = explain_math_concept(topic, student_mistakes)

        if result:
            logging.info(f"Explained concept: {result}")
            print("Explained concept:", result)  # Debugging print
            return jsonify({'result': result})
        else:
            return jsonify({'error': 'Failed to explain concept'}), 500

    except Exception as e:
        logging.exception("Error processing concept explanation request")
        return jsonify({'error': str(e)}), 500

@app.route('/reinforce_resources', methods=['POST'])
def reinforce_resources_api():
    """API endpoint to reinforce concepts with resources."""
    try:
        data = request.get_json()
        logging.info(f"Received data for resources: {data}")
        print("Received data for resources:", data)  # Debugging print

        if not data or not all(key in data for key in ('topic', 'mistake_count')):
            return jsonify({'error': 'Missing required fields'}), 400

        topic = data.get('topic')
        mistake_count = data.get('mistake_count')
        result = reinforce_concept_with_resources(topic, mistake_count)

        if result:
            logging.info(f"Reinforced resources: {result}")
            print("Reinforced resources:", result)  # Debugging print
            return jsonify({'result': result})
        else:
            return jsonify({'error': 'Failed to reinforce resources'}), 500

    except Exception as e:
        logging.exception("Error processing resource request")
        return jsonify({'error': str(e)}), 500

# Add this route for testing
@app.route('/test_data', methods=['POST'])
def test_data_api():
    """API endpoint for testing data transfer."""
    data = request.get_json()
    logging.info(f"Test data received: {data}")
    print("Test data received:", data)  # Debugging print
    return jsonify(data)

@app.route('/script.js')
def serve_js():
    return send_from_directory('static', 'script.js')

@app.route('/js/script.js')  # If it's in a js subfolder
def serve_js_in_folder():
    return send_from_directory('static', 'js/script.js')

if __name__ == '__main__':
    app.run(debug=True)