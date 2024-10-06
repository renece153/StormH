from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "API key"

# Simulated database for job listings
jobs = [
    {"title": "Backend Developer", "description": "Develop REST APIs", "hrEmail": "hr@techcorp.com"},
    {"title": "Frontend Developer", "description": "Develop React applications", "hrEmail": "hr@webcorp.com"},
    {"title": "DevOps Engineer", "description": "Manage CI/CD pipelines", "hrEmail": "hr@cloudservice.com"}
]

@app.route('/match', methods=['POST'])
def match():
    # Get the user's experience and skills from the request
    content = request.json
    experience = content.get('experience', '')
    skills = content.get('skills', '')

    # Create a prompt for OpenAI to find matching jobs
    prompt = f'From the following experience and skills, identify jobs that match:\nExperience: {experience}\nSkills: {skills}\n\nJobs:\n{jobs_to_string(jobs)}'
    
    # Call OpenAI API to process the prompt
    openai_response = call_openai(prompt)
    response_text = openai_response['choices'][0]['text']

    # Extract matched jobs from the response
    matched_jobs = extract_matched_jobs(response_text, jobs)

    return jsonify(matched_jobs)

@app.route('/jobs', methods=['GET'])
def get_jobs():
    return jsonify(jobs)

def jobs_to_string(jobs):
    formatted_jobs = ""
    for job in jobs:
        formatted_jobs += f'Title: {job["title"]}\nDescription: {job["description"]}\n\n'
    return formatted_jobs

def extract_matched_jobs(response_text, jobs):
    matches = []
    for job in jobs:
        if job['title'].lower() in response_text.lower():
            matches.append(job)
    return matches

def call_openai(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=200
    )
    return response

if __name__ == '__main__':
    app.run(port=8080)