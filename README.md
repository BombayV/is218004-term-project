# is218004-term-project
Term project created by group 5 for IS218004. Game review web application using Django, Tailwind CSS, and shadcn-django.

## Prerequisites

- Python 3.12+
- Node.js (for Tailwind CSS)
- Docker & Docker Compose (optional, for containerized development)

## Local Development Setup

1. **Set up the virtual environment and install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Install Node dependencies for Tailwind CSS:**
   ```bash
   npm install
   ```

3. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Start the development server:**
   ```bash
   # Terminal 1: Run the Django Web Server
   python manage.py runserver

   # Terminal 2: Run the Tailwind watch process
   npx @tailwindcss/cli -i input.css -o gamereviews/static/css/output.css --watch
   ```

## Docker Development Setup

1. **Build and start the application using Docker Compose:**
   ```bash
   docker-compose up --build
   ```
   This will automatically start the Django development server on port 8000 and run the Tailwind CSS watcher in the background.

2. **Running migrations or manage.py commands:**
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```
