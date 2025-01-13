# Quiz Application

This is a Django-based quiz application built as part of a technical assessment. The app allows users to sign up, view quizzes, and attempt them.

## Features
- User authentication (sign up, log in, log out)
- Dynamic quiz listing and questions
- Deployed on Render

## Deployment Link
Access the live application here:  https://quiz-app-wt77.onrender.com

## Prerequisites
Ensure you have the following installed:
- Python 3.10+
- pip
- git

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone [Insert Repository URL]
   cd quiz_app


2.Create a virtual environment and activate it:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


3.Install dependencies:
bash
Copy code
pip install -r requirements.txt
Run migrations:

4.bash
Copy code
python manage.py migrate
Start the development server:

5.bash
Copy code
python manage.py runserver
6.Open the app in your browser at http://127.0.0.1:8000.



Static Files
Ensure you have collected the static files before deployment:
bash
Copy code
python manage.py collectstatic

Repository Structure
quiz_app/: Django project folder
quizzes/: Main app handling quiz functionality
static/: Static files (CSS, JS, etc.)
templates/: HTML templates for the application

License
This project is for educational purposes only.

