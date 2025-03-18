// script.js

function generateStudyPlan() {
    console.log("generateStudyPlan function called");

    const gradeLevel = document.getElementById('gradeLevel').value;
    const weakTopics = document.getElementById('weakTopics').value;
    const availableHours = document.getElementById('availableHours').value;

    console.log("Sending data:", { grade_level: gradeLevel, weak_topics: weakTopics, available_hours: availableHours });

    fetch('/generate_study_plan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            grade_level: gradeLevel,
            weak_topics: weakTopics,
            available_hours: availableHours
        })
    })
    .then(response => {
        console.log("Response from server:", response);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log("Data from server:", data);
        if (data && data.result) { // Check if data and data.result exist
            document.getElementById('studyPlanOutput').textContent = data.result;
        } else if (data && data.error) { // Check if data and data.error exist
            document.getElementById('studyPlanOutput').textContent = "Error: " + data.error;
        } else {
            document.getElementById('studyPlanOutput').textContent = "Unexpected response format";
        }
    })
    .catch(error => {
        console.error("There was a problem with the fetch operation:", error);
        document.getElementById('studyPlanOutput').textContent = "Error: " + error.message;
    });
}

function generateQuestions() {
    console.log("generateQuestions function called");

    const topic = document.getElementById('topic').value;
    const difficulty = document.getElementById('difficulty').value;
    const previousMistakes = document.getElementById('previousMistakes').value;

    console.log("Sending data:", { topic: topic, difficulty: difficulty, previous_mistakes: previousMistakes });

    fetch('/generate_questions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            topic: topic,
            difficulty: difficulty,
            previous_mistakes: previousMistakes
        })
    })
    .then(response => {
        console.log("Response from server:", response);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log("Data from server:", data);
        if (data && data.result) {
            document.getElementById('questionsOutput').textContent = data.result;
        } else if (data && data.error) {
            document.getElementById('questionsOutput').textContent = "Error: " + data.error;
        } else {
            document.getElementById('questionsOutput').textContent = "Unexpected response format";
        }
    })
    .catch(error => {
        console.error("There was a problem with the fetch operation:", error);
        document.getElementById('questionsOutput').textContent = "Error: " + error.message;
    });
}

function explainConcept() {
    console.log("explainConcept function called");

    const topic = document.getElementById('conceptTopic').value;
    const studentMistakes = document.getElementById('conceptMistakes').value;

    console.log("Sending data:", { topic: topic, student_mistakes: studentMistakes });

    fetch('/explain_concept', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            topic: topic,
            student_mistakes: studentMistakes
        })
    })
    .then(response => {
        console.log("Response from server:", response);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log("Data from server:", data);
        if (data && data.result) {
            document.getElementById('conceptOutput').textContent = data.result;
        } else if (data && data.error) {
            document.getElementById('conceptOutput').textContent = "Error: " + data.error;
        } else {
            document.getElementById('conceptOutput').textContent = "Unexpected response format";
        }
    })
    .catch(error => {
        console.error("There was a problem with the fetch operation:", error);
        document.getElementById('conceptOutput').textContent = "Error: " + error.message;
    });
}

function reinforceResources() {
    console.log("reinforceResources function called");

    const topic = document.getElementById('resourceTopic').value;
    const mistakeCount = document.getElementById('resourceMistakes').value;

    console.log("Sending data:", { topic: topic, mistake_count: mistakeCount });

    fetch('/reinforce_resources', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            topic: topic,
            mistake_count: mistakeCount
        })
    })
    .then(response => {
        console.log("Response from server:", response);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log("Data from server:", data);
        if (data && data.result) {
            document.getElementById('resourceOutput').textContent = data.result;
        } else if (data && data.error) {
            document.getElementById('resourceOutput').textContent = "Error: " + data.error;
        } else {
            document.getElementById('resourceOutput').textContent = "Unexpected response format";
        }
    })
    .catch(error => {
        console.error("There was a problem with the fetch operation:", error);
        document.getElementById('resourceOutput').textContent = "Error: " + error.message;
    });
}

// Add this function for testing
function testData() {
    console.log("testData function called");

    fetch('/test_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: "Hello from JavaScript!" })
    })
    .then(response => {
        console.log("Response from server:", response);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log("Data from server:", data);
    })