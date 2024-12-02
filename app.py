from flask import Flask, render_template, request
import google.generativeai as genai
import os

# Установка API ключа для Google Gemini
os.environ["GOOGLE_API_KEY"] = "AIzaSyCrxXOE4h3nfOHGatKQYCxVH089hwmlDZo"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)

# Функция для генерации курса
def generate_course_content(course_description):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(course_description)

        if response.candidates:
            return response.candidates[0].content.parts[0].text
        else:
            return "Ошибка: Ответ не был получен"
    except Exception as e:
        return f"Ошибка: Не удалось подключиться к сервису. Детали: {str(e)}"

# Проверка на ключевые слова, связанные с курсом
def is_course_related(text):
    keywords = ["курс", "учебный", "лекция", "обучение", "тема"]
    return any(keyword in text.lower() for keyword in keywords)

@app.route('/')
def index():
    return render_template('index.html')

# Маршрут для генерации контента
@app.route('/generate-course', methods=['POST'])
def generate_course():
    course_description = request.form['course_description']
    content_type = request.form.get('contentType', 'course')

    # Уточнение запроса в зависимости от типа контента
    if content_type == "course" and not is_course_related(course_description):
        course_description = f"Создай учебный курс по теме: {course_description}"
    elif content_type == "lecture":
        course_description = f"Создай лекцию по теме: {course_description}"
    elif content_type == "answer":
        course_description = f"Ответь на вопрос: {course_description}"

    # Генерация курса и передача его в шаблон
    course_content = generate_course_content(course_description)
    return render_template("result.html", course_content=course_content)

if __name__ == '__main__':
    app.run(debug=True)
