# Storage Management System

A full-stack inventory management application built with Django REST Framework, PostgreSQL and JavaScript. Authenticated users can manage products, track inventory, process orders, review stock movements, and ask an AI-powered chatbot questions about their store in plain English.

## Features

- **Authentication:** Login and logout with JWT-based authentication.
- **Role-based users:** Custom user model with Admin and Staff roles.
- **Product management:** Create, view, update and delete products.
- **Inventory tracking:** Monitor stock quantities and spot low-stock products.
- **Order management:** Orders deduct stock automatically inside a database transaction, with handling for insufficient stock. Stock is restored when an order is deleted.
- **Stock movement history:** Every incoming and outgoing movement is recorded along with its reason.
- **Dashboard:** Inventory summary and recent stock activity at a glance.
- **AI chatbot:** Ask natural-language questions about products, stock levels, low-stock items, orders and recent stock movements.
- **REST API:** Built with Django REST Framework and returns JSON.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python, Django |
| API | Django REST Framework |
| Authentication | Simple JWT |
| Database | PostgreSQL |
| Frontend | HTML, CSS, JavaScript |
| Chatbot model | Ollama with Qwen 2.5 (1.5B), accessed through the OpenAI-compatible API |
| Containerization | Docker and Docker Compose (see the note in [Docker Setup](#docker-setup)) |

## How It Works

The frontend sends requests to the Django REST API. Django handles authentication, business logic and database access. The chatbot works out what the user is asking (the intent), fetches the matching data from the database, and answers from that data. A locally hosted language model is used to classify the intent.

## Project Structure

```
StorageManagementSystem/
├── users/            # custom user model, roles, JWT auth
├── products/         # product model and API
├── inventory/        # stock quantities
├── orders/           # orders and stock deduction
├── stock_history/    # stock movement records
├── chatbot/          # chatbot logic
├── frontend/         # HTML, CSS and JavaScript pages
├── store_management/ # Django project settings and URLs
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## Prerequisites

- Python 3
- PostgreSQL
- Git
- [Ollama](https://ollama.com) (optional, only needed for the chatbot)
- Docker Desktop (optional, only for the Docker setup)

## Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/shivangi-bis/StorageManagementSystem.git
cd StorageManagementSystem
```

### 2. Create and activate a virtual environment

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the PostgreSQL database

Create an empty database for the project, for example:

```sql
CREATE DATABASE storage_management;
```

### 5. Configure environment variables

Copy the example file and fill in your own values.

Windows:

```powershell
copy .env.example .env
```

macOS / Linux:

```bash
cp .env.example .env
```

| Variable | Purpose |
|----------|---------|
| `DJANGO_SECRET_KEY` | Django secret key. Use a long random string. |
| `DEBUG` | `True` for local development, `False` in production. |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts. |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | PostgreSQL connection details. |
| `CORS_ALLOWED_ORIGINS` | Comma-separated list of origins allowed to call the API. |
| `OPENAI_API_KEY` | Optional. |
| `OLLAMA_BASE_URL` | Ollama API address. Defaults to `http://localhost:11434/v1`. |

> Never commit your `.env` file. It is already listed in `.gitignore`.

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Create an admin account

```bash
python manage.py createsuperuser
```

### 8. Start the backend

```bash
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/`.

### 9. Open the frontend

The frontend pages are in the `frontend/` folder. Serve them with any local static server (for example the VS Code Live Server extension) and open the login page. If your frontend runs on an origin other than the defaults, add it to `CORS_ALLOWED_ORIGINS` in your `.env`.

## Running the AI Chatbot

Install Ollama, then download the model:

```bash
ollama pull qwen2.5:1.5b
```

Make sure the Ollama service is running and that `OLLAMA_BASE_URL` points to it.

Example questions you can ask:

- How many products do I have?
- How much stock is left?
- What is the stock of Keyboard?
- Which products are running low?
- How many orders do I have?
- Show recent stock movements.

Answers come from the data in your database, so their quality depends on accurate records and on the model recognising the question correctly.

## Testing

Run the automated test suite:

```bash
python manage.py test
```

You can also check that the models and migrations are in sync:

```bash
python manage.py makemigrations --check --dry-run
```

## Docker Setup

> **Note:** Docker configuration is included but has not been fully tested yet. Treat it as experimental.

The `docker-compose.yml` defines a PostgreSQL service and the Django web service. Database credentials are read from your `.env` file, and the web container reaches Ollama on the host through `host.docker.internal`.

```bash
docker compose build
docker compose up -d
docker compose logs -f
```

Stop the containers with:

```bash
docker compose down
```

Avoid deleting Docker volumes unless you want to erase the stored database data.

## Security Notes

- Keep `.env` and all credentials out of version control.
- Use a long random `DJANGO_SECRET_KEY`. When `DEBUG=False`, the app refuses to start without one.
- Before any public deployment, set `DEBUG=False`, a valid `ALLOWED_HOSTS` and a restricted `CORS_ALLOWED_ORIGINS`. Cross-origin access is open to all origins only while `DEBUG=True`.
- Do not expose the database port unnecessarily.
- If a key or password is ever exposed, revoke it and create a new one.

## Future Improvements

- More automated tests for the API endpoints, order processing and the chatbot
- Verified Docker workflow
- Production deployment
- Better chatbot intent recognition and error handling
- Detailed inventory reports and analytics

## Author

**Shivangi Biswas**

GitHub: [shivangi-bis](https://github.com/shivangi-bis)