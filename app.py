import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
import markdown


app = Flask(__name__)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_code', methods=['POST'])
def submit_code():
    language = request.form['language'] 

    if 'codeFile' in request.files:
        code_file = request.files['codeFile']
        code = code_file.read().decode('utf-8')  
    else:
        code = request.form['code'] 
    
    feedback = get_groq_feedback(code, language)
    return jsonify({'feedback': feedback})

def get_groq_feedback(code,language):
    try:
        system_message = """
As a detailed code reviewer, thoroughly assess the code below according to the following points:
    * Use the 🚨 emoji to indicate high-priority suggestions, listed from the most important to the least.
    * Provide a clear and concise summary of the code.
    * Offer actionable feedback on the code's structure, syntax, and best practices.
    * There should enough gap between each point you  are mentioning.
    * Lenght of feedback direclty depend on length of code
    * Whenever possible, provide examples of improvements by showing a 'before and after' version.
    * Calmly walk through your reasoning step-by-step for each suggestion you make.
"""
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"Review the following {language} code:\n{code}"}
            ],
            model="llama3-8b-8192",
        )

        feedback = chat_completion.choices[0].message.content
        html_feedback = markdown.markdown(feedback)
    except Exception as e:
        html_feedback = f"Error: {str(e)}"
    
    return html_feedback

if __name__ == '__main__':
    app.run(debug=True)
