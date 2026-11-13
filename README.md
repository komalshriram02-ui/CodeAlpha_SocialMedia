# Linkup - Social Media Platform

A full stack social media web application built with **Django** and **PostgreSQL** as part of the CodeAlpha Full Stack Development internship (Task 2).

## Features

- User registration, login and logout
- User profiles with bio and profile photo
- Create posts with text and images
- Like posts (heart button) and comment on posts
- Follow and unfollow users, with followers and following counts
- Home feed showing posts from people you follow
- Search users by username
- Delete your own posts
- Instagram style bottom navigation bar



## Tech Stack

- **Backend:** Python, Django
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, Django Templates



## Setup Instructions

1. Clone the repository

   ```
   git clone https://github.com/komalshriram02-ui/CodeAlpha_SocialMedia.git
   cd CodeAlpha_SocialMedia
   ```

2. Create and activate a virtual environment

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies

   ```
   pip install django psycopg2-binary pillow python-dotenv
   ```

4. Create a PostgreSQL database named `social_db`

5. Copy `.env.example` to `.env` and add your PostgreSQL password

   ```
   copy .env.example .env
   ```

6. Run migrations

   ```
   python manage.py migrate
   ```

7. Start the server

   ```
   python manage.py runserver
   ```

Open http://127.0.0.1:8000/accounts/register/ in your browser and create an account.

## Author

Komal Shriram