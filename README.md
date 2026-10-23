# Storage Management System

A full-stack inventory management application built with Django REST Framework, PostgreSQL, and JavaScript. It helps manage products, track inventory, process orders, record stock movements, and retrieve inventory information through a database-aware chatbot.

## Features

- **JWT Authentication:** Authenticated access using JSON Web Tokens.
- **Product Management:** Create, view, update, and delete products.
- **Inventory Tracking:** Monitor stock quantities and identify low-stock products.
- **Order Management:** Create and update orders with automatic inventory adjustments.
- **Stock Restoration:** Restore inventory when an order is deleted.
- **Stock Movement History:** Record incoming and outgoing stock movements with reasons.
- **Dashboard:** View inventory summaries and recent stock activity.
- **Inventory Chatbot:** Ask questions about products, stock levels, low-stock items, orders, and recent stock movements.
- **REST API:** API endpoints built using Django REST Framework.
- **PostgreSQL Database:** Persistent relational data storage.
- **Docker Support:** Dockerfile and Docker Compose configuration for containerized development.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Django |
| API | Django REST Framework |
| Authentication | Simple JWT |
| Database | PostgreSQL |
| Frontend | HTML, CSS, JavaScript |
| Chatbot LLM | Ollama with Qwen 2.5 (1.5B) |
| API Format | REST / JSON |
| Containerization | Docker, Docker Compose |

## Architecture

The frontend communicates with the Django REST API. Django handles authentication, application logic, and database operations. The inventory chatbot interprets supported questions and retrieves information from application data. When configured and available, a locally hosted language model assists with natural-language intent handling.

## Project Structure

```text
StorageManagementSystem/
├── users/
├── products/
├── orders/
├── inventory/
├── stock_history/
├── chatbot/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

*This is a high-level overview. The exact files may vary with the current repository structure.*

## Prerequisites

For local development:

- Python version compatible with the project dependencies
- PostgreSQL
- Git
- Ollama, if using the local language model

For containerized development:

- Docker Desktop
- Docker Compose

## Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/shivangi-bis/StorageManagementSystem.git
cd StorageManagementSystem
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Configure the environment variables required by the project, including the Django secret key and PostgreSQL connection settings.

Use a local `.env` file if the project configuration expects one. Never commit real credentials or secrets to version control.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Create an administrator account

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` and navigate to the appropriate application page or API endpoint.

## Running the Chatbot

Install Ollama and download the configured model:

```bash
ollama pull qwen2.5:1.5b
```

Start Ollama and ensure the chatbot's configured model name and API endpoint match the running service. If the application runs inside Docker, configure the Ollama host address so the container can reach the host service.

Example questions:

- How many products do I have?
- How much stock is left?
- What is the stock of Keyboard?
- Which products are running low?
- How many orders do I have?
- Show recent stock movements.

Chatbot responses depend on the available database records, supported intents, and successful communication with the language model when required.

## Docker Setup

Build and start the containers:

```bash
docker compose build
docker compose up -d
```

Check container status and logs:

```bash
docker compose ps
docker compose logs -f
```

Stop the containers:

```bash
docker compose down
```

Do not remove database volumes unless you intentionally want to delete persisted database data.

**Development note:** Verify the Docker configuration and end-to-end application behavior in the target environment before relying on it. The Django development server (`runserver`) is not intended for production deployment.

## Automated Tests

The project currently includes automated tests for selected user permissions and order/inventory workflows.

Run all tests:

```bash
python manage.py test
```

The current test suite covers:

- Staff users cannot view the complete user list.
- Staff users cannot create or delete users.
- Staff users can view their own user details.
- Creating an order reduces inventory stock.
- Orders exceeding available stock are rejected.
- Deleting an order restores inventory stock.

These tests verify selected workflows; they do not represent complete coverage of every API endpoint or concurrent request scenario.

## Security Considerations

- Keep `.env` files and credentials out of version control.
- Store secret keys and database credentials in environment variables.
- Configure `DEBUG=False`, valid `ALLOWED_HOSTS`, HTTPS, and other production security settings before public deployment.
- Restrict database access and avoid exposing database ports unnecessarily.
- Protect authenticated endpoints and validate incoming requests.
- Review role-based permissions and password handling when changing user-management functionality.

## Deployment

The application can be prepared for a hosting platform that supports Django and PostgreSQL. Production deployment requires suitable environment configuration, database provisioning, static-file handling, HTTPS, and a production application server.

No public deployment URL is listed here because a deployment should be verified before being advertised.

## Future Improvements

- Expand automated tests for authentication, product endpoints, inventory, and chatbot responses.
- Add automated concurrency tests for simultaneous order requests.
- Improve chatbot error handling and intent recognition.
- Add inventory reports and analytics.
- Configure and verify a production-ready Docker deployment.

## Author

**Shivangi Biswas**

GitHub: [shivangi-bis](https://github.com/shivangi-bis)
