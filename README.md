# Storage Management System

A full-stack inventory management application built with Django REST Framework, PostgreSQL, and JavaScript. It provides product management, inventory tracking, order processing, stock movement history, and a database-aware chatbot for inventory-related queries.

## Features

- **JWT Authentication:** Token-based authentication using Simple JWT.
- **Product Management:** Create, retrieve, update, and delete products.
- **Inventory Management:** Track stock quantities and identify low-stock products.
- **Order Processing:** Manage orders with automatic inventory deduction.
- **Stock Restoration:** Restore inventory when an order is deleted.
- **Stock Movement History:** Record incoming and outgoing stock movements with reasons.
- **Dashboard:** View inventory summaries and recent stock activity.
- **Inventory Chatbot:** Ask natural-language questions about products, stock levels, orders, and stock movements.
- **REST API:** Access application functionality through Django REST Framework endpoints.
- **PostgreSQL Integration:** Store application data in a relational database.
- **Docker Configuration:** Includes Docker and Docker Compose configuration for containerized setup.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | Django |
| REST API | Django REST Framework |
| Authentication | Simple JWT |
| Database | PostgreSQL |
| Frontend | HTML, CSS, JavaScript |
| Chatbot | Ollama, Qwen 2.5 (1.5B) |
| API Communication | REST / JSON |
| Containerization | Docker, Docker Compose |

## Architecture

The frontend communicates with the Django REST API. Django handles authentication, business logic, and database operations, while PostgreSQL stores application data.

The chatbot processes supported natural-language questions and retrieves relevant information from the application database. Ollama provides local language-model support for intent handling.

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
├── .env.example
└── README.md
```

## Prerequisites

- Python
- PostgreSQL
- Git
- Ollama (for local language-model functionality)
- Docker Desktop (for containerized setup)

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/shivangi-bis/StorageManagementSystem.git
cd StorageManagementSystem
```

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a local `.env` file using `.env.example` as a reference. Configure the Django secret key, PostgreSQL database credentials, allowed hosts, and other settings required by the application.

Ensure PostgreSQL is running and the configured database exists before proceeding.

Never commit real credentials or secret keys to GitHub.

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Create an Administrator Account

```bash
python manage.py createsuperuser
```

### 7. Start the Development Server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser and navigate to the appropriate application page or API endpoint.

## Chatbot Setup

Install Ollama and download the configured model:

```bash
ollama pull qwen2.5:1.5b
```

Start Ollama and ensure the chatbot's configured model name and API endpoint match the running service.

Example questions:

- How many products do I have?
- How much stock is left?
- What is the stock of Keyboard?
- Which products are running low?
- How many orders do I have?
- Show recent stock movements.

The chatbot uses application data to answer supported inventory-related questions.

## Docker Setup

The repository includes a `Dockerfile` and a Docker Compose configuration.

Build and start the configured services:

```bash
docker compose up --build
```

Check the service status:

```bash
docker compose ps
```

View service logs:

```bash
docker compose logs -f
```

Stop the services:

```bash
docker compose down
```

## Running Tests

Run the Django test suite:

```bash
python manage.py test
```

The automated tests cover selected permission and inventory workflows, including:

- Staff user permissions.
- Inventory deduction when an order is created.
- Rejection of orders exceeding available stock.
- Inventory restoration when an order is deleted.

## Security

- Keep secret keys and database credentials in environment variables.
- Do not commit `.env` files containing sensitive information.
- Configure production security settings before exposing the application publicly.
- Use appropriate authentication and permissions for protected API endpoints.

## Author

**Shivangi Biswas**

GitHub: [shivangi-bis](https://github.com/shivangi-bis)

Project Repository: [Storage Management System](https://github.com/shivangi-bis/StorageManagementSystem)
