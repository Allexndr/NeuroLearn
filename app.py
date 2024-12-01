from flask import Flask, render_template, request
import google.generativeai as genai
import os

os.environ["GOOGLE_API_KEY"] = ""
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)

def generate_course_content(course_description):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(course_description)

    if response.candidates:
        return response.candidates[0].content.parts[0].text
    else:
        return "Ошибка: Ответ не был получен"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-course', methods=['POST'])
def generate_course():
    course_description = request.form['course_description']
    course_content = generate_course_content(course_description)
    return f"Generated Course Content: {course_content}"

if __name__ == '__main__':
    app.run(debug=True)
