from flask import Flask, render_template, request, redirect, url_for, flash, session
import google.generativeai as genai
import os
import requests
from markupsafe import Markup

# Настройка API ключей
os.environ["GOOGLE_API_KEY"] = "AIzaSyCrxXOE4h3nfOHGatKQYCxVH089hwmlDZo"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = 'supersecretkey'

# Функция для форматирования текста курса
def format_course_content(raw_content):
    formatted_content = raw_content.replace("**", "").replace("*", "")
    formatted_content = formatted_content.replace("##", "<h3>").replace(":", "</h3>")
    formatted_content = formatted_content.replace("*", "<li>").replace(".", "</li>")
    formatted_content = f"<div class='course-content'>{formatted_content}</div>"
    return Markup(formatted_content)

# Функция для получения изображений с Unsplash
def get_image_for_topic(topic):
    try:
        response = requests.get(
            "https://api.unsplash.com/photos/random",
            params={"query": topic, "client_id": "YOUR_UNSPLASH_API_KEY"}
        )
        data = response.json()
        return data['urls']['regular']
    except Exception as e:
        return "/static/images/default.jpg"

# Функция для получения видео с YouTube
def get_videos_for_topic(topic):
    try:
        api_key = "YOUR_YOUTUBE_API_KEY"
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

# Функция для получения полезных ссылок
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

# Генерация курса
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-course', methods=['POST'])
def generate_course():
    course_title = request.form['course_title']
    course_description = request.form['course_description']
    content_type = request.form.get('contentType', 'course')

    if content_type == "course":
        course_description = f"Создай учебный курс по теме: {course_description}"
    elif content_type == "lecture":
        course_description = f"Создай лекцию по теме: {course_description}"
    elif content_type == "answer":
        course_description = f"Ответь на вопрос: {course_description}"

    # Генерация курса
    raw_content = generate_course_content(course_description)
    course_content = format_course_content(raw_content)

    # Динамическое наполнение
    course_image = get_image_for_topic(course_description)
    course_videos = get_videos_for_topic(course_description)
    course_links = get_links_for_topic(course_description)

    return render_template(
        "result.html",
        course_title=course_title,
        course_content=course_content,
        course_image=course_image,
        course_videos=course_videos,
        course_links=course_links
    )

if __name__ == '__main__':
    app.run(debug=True)
