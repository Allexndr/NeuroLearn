# Course Generator with Google Gemini and Flask

This project is a web application built using Flask, which leverages Google Gemini for course content generation, Unsplash for thematic images, YouTube API for video content, and Bing API for helpful links. The app allows users to generate a custom course based on a given topic, displaying content such as lessons, images, videos, and external resources.

## Features

- **Course Content Generation**: Uses Google Gemini API to generate detailed course content based on the topic provided by the user.
- **Dynamic Course Layout**: The content is automatically formatted into modules and lessons with theory, practice, and additional resources.
- **Thematic Images**: Fetches relevant images from Unsplash based on the topic of the course.
- **YouTube Videos**: Retrieves related YouTube videos for the generated course.
- **Useful Links**: Fetches helpful resources and links using Bing's search API.
- **User Authentication**: Allows users to log in, view their profile, and log out.

## Technologies Used

- **Flask**: A micro web framework for building the web application.
- **Google Gemini**: For generating course content based on the provided topic.
- **Unsplash API**: For retrieving thematic images related to the course topic.
- **YouTube Data API**: For fetching relevant videos related to the course topic.
- **Bing API**: For fetching helpful external links based on the course topic.

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/course-generator-flask.git
2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
3. **Set up your API keys:**
   - **Google Gemini API Key**: Set up your key and configure it in the GOOGLE_API_KEY environment variable.
   - **Unsplash API Key**: Set up your Unsplash API key and replace the placeholder in the code.
   - **Bing API Key**: Set up your Bing Search API key and replace the placeholder in the code.
   - **YouTube API Key**: Set up your YouTube API key and replace the placeholder in the code.
4. **Run the application:**
   ```bash
   python app.py
## Endpoints

- `/`: The homepage, where users can input the topic to generate a course.
- `/generate`: Generates a course based on the provided topic and displays results.
- `/about`: Information about the project.
- `/blog`: Blog page.
- `/prices`: Pricing details for the service.
- `/contact`: Contact information page.
- `/profile`: User profile page (requires login).
- `/login`: Logs the user in and redirects to the profile.
- `/logout`: Logs the user out and redirects to the homepage.
