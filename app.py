
from flask import Flask, render_template, request, redirect, url_for, session, flash
import google.generativeai as genai
import os
import requests
from markupsafe import Markup
from flask_sqlalchemy import SQLAlchemy

# Настройка API ключей
os.environ["GOOGLE_API_KEY"] = "AIzaSyCrxXOE4h3nfOHGatKQYCxVH089hwmlDZo"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = "supersecretkey"

#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://:password@localhost/your_database'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# Модель пользователя
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)
# #
# # Маршруты
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#
#         new_user = User(username=username, email=email, password=password)
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('login'))
#     return render_template('signup.html')
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         user = User.query.filter_by(email=email, password=password).first()
#         if user:
#             return f"Welcome, {user.username}!"
#         return "Invalid credentials. Try again."
#     return render_template('login.html')


# ==============================
# Вспомогательные функции
# ==============================

# Форматирование контента курса
def format_course_content(raw_content):
    try:
        # Разбиваем текст на модули
        modules = raw_content.split("Модуль")
        formatted_content = ""

        for i, module in enumerate(modules):
            if module.strip():
                # Заголовок модуля
                module_lines = module.strip().split("\n")
                module_title = module_lines[0] if module_lines else f"Модуль {i+1}"
                formatted_content += f"<h2>Модуль {module_title.strip()}</h2>"

                # Разбиваем уроки внутри модуля
                lessons = module.split("Урок")
                for j, lesson in enumerate(lessons):
                    if lesson.strip():
                        lesson_lines = lesson.strip().split("\n")
                        lesson_title = lesson_lines[0] if lesson_lines else f"Урок {j+1}"
                        formatted_content += f"<h3>Урок {lesson_title.strip()}</h3>"

                        # Добавляем наполнение урока
                        formatted_content += "<p><strong>Теория:</strong> Изучите основы этой темы.</p>"
                        formatted_content += "<p><strong>Практика:</strong> Выполните задание, чтобы закрепить материал.</p>"
                        formatted_content += "<p><strong>Дополнительные ресурсы:</strong></p>"
                        formatted_content += """
                        <ul>
                            <li><a href="https://example.com" target="_blank">Полезный сайт 1</a></li>
                            <li><a href="https://example.com" target="_blank">Полезный сайт 2</a></li>
                        </ul>
                        """

        # Возвращаем отформатированный текст
        return Markup(f"<div class='course-content'>{formatted_content}</div>")
    except Exception as e:
        print(f"Ошибка форматирования: {e}")
        return Markup(f"<p>{raw_content}</p>")

# Генерация курса через Google Gemini
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

# Получение тематического изображения с Unsplash
def get_image_for_topic(topic):
    try:
        response = requests.get(
            "https://api.unsplash.com/photos/random",
            params={
                "query": topic,
                "client_id": "A0DjwN9LCDJ2ZWUcdNeqaqzMQ6O10tSTDKi86Im3z6M"  # Replace with your actual Unsplash API key
            }
        )
        if response.status_code == 200:
            data = response.json()
            print(f"Unsplash API Response: {data}")  # Debug response
            return data['urls']['regular']
        else:
            print(f"Unsplash API Error: {response.status_code} - {response.text}")
            return "/static/images/default.jpg"  # Default fallback image
    except Exception as e:
        print(f"Error fetching image: {e}")
        return "/static/images/default.jpg"


# Получение видео с YouTube
def get_videos_for_topic(topic):
    try:
        api_key = "AIzaSyB_4t_dhe5vNifnVhbwAxhzT8NDE0cBFag"
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={topic}&type=video&key={api_key}&maxResults=3"
        response = requests.get(url)
        data = response.json()
        videos = [
            {
                "title": item["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }
            for item in data.get("items", [])
        ]
        return videos
    except Exception as e:
        return []

# Получение полезных ссылок через Bing API
def get_links_for_topic(topic):
    try:
        headers = {"Ocp-Apim-Subscription-Key": "YOUR_BING_API_KEY"}
        params = {"q": topic, "count": 5}
        response = requests.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params)
        data = response.json()
        links = [
            {"title": item["name"], "url": item["url"]}
            for item in data.get("webPages", {}).get("value", [])
        ]
        return links
    except Exception as e:
        return []

# ==============================
# Маршруты
# ==============================

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Генерация курса
@app.route('/generate', methods=['POST', 'GET'])
def generate():
    if request.method == 'POST':
        topic = request.form.get('topic')
    else:
        topic = request.args.get('topic', 'Курс по умолчанию')

    course_description = f"Создай учебный курс по теме: {topic}"
    raw_content = generate_course_content(course_description)
    course_content = format_course_content(raw_content)
    course_images = [get_image_for_topic(topic) for _ in range(3)]  # Generate 3 images
    course_videos = get_videos_for_topic(topic)
    course_links = get_links_for_topic(topic)

    # Debug output for images
    print(f"Generated Images: {course_images}")

    return render_template(
        "results.html",
        course_title=topic,
        course_content=course_content,
        course_images=course_images,
        course_videos=course_videos,
        course_links=course_links
    )




# Страница "О проекте"
@app.route('/about')
def about():
    return render_template('about.html')
@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/prices")
def prices():
    return render_template("prices.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")
# Страница тарифов
@app.route('/pricing')
def pricing():
    return render_template('prices.html')

# Личный кабинет
@app.route('/profile')
def profile():
    if 'user' in session:
        return render_template('profile.html', user=session['user'])
    return redirect(url_for('login'))
@app.route('/courses')
def courses():
    return render_template('courses.html')
# Вход в аккаунт
@app.route('/login')
def login():
    session['user'] = {'name': 'Demo User', 'plan': 'Free'}
    flash('Вы успешно вошли в систему!', 'success')
    return redirect(url_for('profile'))

# Выход из аккаунта
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('index'))

# ==============================
# Запуск приложения
# ==============================

if __name__ == '__main__':
    app.run(debug=True)
