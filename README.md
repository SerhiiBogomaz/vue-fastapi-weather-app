# Weather App

This project is a web application for displaying current weather by city. Users can register, add or edit their OpenWeather API key, and view up-to-date weather information for any city.

## Features

- User registration and authentication
- Profile editing, including avatar upload
- Personal OpenWeather API key management
- Get current weather by city

## Quick Start: Run with Docker

### 1. Clone the repository

```sh
git clone <your-repository-url>
cd <your-repository>
```

### 2. Create environment files

Copy the example environment files and fill in your values:

```sh
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

**Important:**
Add your OpenWeather API key to the `OPENWEATHER_API_KEY` variable in `backend/.env`.
You can get a free API key at [api.openweathermap.org](https://api.openweathermap.org/).

Example:

```env
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_database_name
DATABASE_URL=postgresql+asyncpg://your_postgres_user:your_postgres_password@db:5432/your_database_name
SECRET_KEY=your_secret_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

In `frontend/.env` set the backend server address:

```env
VITE_API_URL=http://localhost:8000
```

### 3. Start the project with Docker

```sh
docker compose up --build
```

This will start the backend, frontend, and database.

### 4. Open the app

Open your browser and go to [http://localhost:5173](http://localhost:5173) (or another port if configured).

Or, from the terminal:

```sh
"$BROWSER" http://localhost:5173
```

## How to get an OpenWeather API key

1. Register at [https://api.openweathermap.org](https://api.openweathermap.org).
2. Go to the API Keys section in your account.
3. Copy your generated key and add it to your profile during registration or profile editing in the app.

**You can add or update your API key in your user profile via the app interface.**

## Main commands

- Start all services:
  ```sh
  docker compose up --build
  ```
- Stop all services:
  ```sh
  docker compose down
  ```

## Project structure

- `backend/` — FastAPI backend
- `frontend/` — Vue.js frontend
- `docker-compose.yml` — Docker configuration

---

If you have questions, check the comments in `.env.example` or see the
