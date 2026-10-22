# Storage Management System

A full-stack inventory management application built with Django REST Framework, PostgreSQL, and JavaScript. The application enables authenticated users to manage products, monitor inventory, process orders, track stock movements, and query inventory information through an AI-powered chatbot.

## Features

- **Authentication:** User login and logout with JWT-based authentication.
- **Product Management:** Create, view, update, and delete products.
- **Inventory Tracking:** Monitor stock quantities and identify low-stock products.
- **Order Management:** Process orders with automatic stock deduction and stock restoration when an order is deleted.
- **Stock Movement History:** Track incoming and outgoing stock movements and their reasons.
- **Dashboard:** View inventory summaries and recent stock activity.
- **AI-Powered Chatbot:** Ask natural-language questions about products, available stock, low-stock items, orders, and recent stock movements.
- **REST API:** Backend API endpoints built with Django REST Framework.
- **Database:** PostgreSQL for persistent application data.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Django |
| API | Django REST Framework |
| Authentication | Simple JWT |
| Database | PostgreSQL |
| Frontend | HTML, CSS, JavaScript |
| Local Language Model | Ollama with Qwen 2.5 (1.5B) |
| API Format | REST / JSON |
| Containerization | Docker and Docker Compose — setup to be verified |

## Application Architecture

The frontend communicates with Django REST API endpoints. Django handles authentication, business logic, and database operations. The chatbot interprets user questions and retrieves relevant inventory information from the database, using a locally hosted language model for intent classification where configured.

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
├── .gitignore
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── README.md
```

*The structure is illustrative. Keep only files and directories that actually exist in the repository.*

## Prerequisites

For local development:

- Python compatible with the project's dependencies
- PostgreSQL
- Git
- Ollama, if you want to run the chatbot with the local language model

For containerized development, Docker Desktop with Docker Compose is also required.

## Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/shivangi-bis/StorageManagementSystem.git
cd StorageManagementSystem
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file using the project's required settings. Configure the Django secret key, database name, database username, database password, host, and port according to the actual application configuration.

Do not commit `.env` or production credentials to version control.

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create an administrator account if needed

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` and navigate to the application's configured login or dashboard page.

## Running the AI Chatbot

Install Ollama and download the configured model:

```bash
ollama pull qwen2.5:1.5b
```

Start the Ollama service and confirm that the model name and local API endpoint match the chatbot configuration.

Example questions:

- How many products do I have?
- How much stock is left?
- What is the stock of Keyboard?
- Which products are running low?
- How many orders do I have?
- Show recent stock movements.

The chatbot relies on application data for inventory-related answers. Its accuracy depends on correct database records, intent recognition, and successful API communication.

## Docker Setup

Docker support should be considered ready only after the `Dockerfile` and `docker-compose.yml` have been implemented and tested with the project's actual configuration.

Once configured, the intended workflow is:

```bash
docker compose build
docker compose up -d
docker compose logs -f
```

The container setup should configure the web application, PostgreSQL connectivity, environment variables, migrations, and the Ollama connection as appropriate. Ollama must be reachable from the application container; `localhost` inside a container refers to that container itself, not automatically to the host machine.

Stop the containers with:

```bash
docker compose down
```

Do not remove database volumes unless you intentionally want to delete the persisted database data.

## Testing

The following core workflows have been manually verified:

- User login and logout
- Product creation, editing, and deletion
- Automatic stock updates when creating an order
- Six chatbot questions returning the expected answers

Manual verification does not replace automated unit, integration, or API tests. Additional automated test coverage can be added for authentication, product endpoints, order processing, stock restoration, and chatbot responses.

## Security Considerations

- Keep `.env` and all credentials out of version control.
- Use environment variables for secret keys and database credentials.
- Use appropriate Django production settings, including `DEBUG=False`, valid `ALLOWED_HOSTS`, and secure HTTPS settings, before public deployment.
- Restrict database access and avoid exposing database ports unnecessarily.
- Protect authenticated API endpoints and validate incoming requests.
- Never publish real credentials, access tokens, or private keys in the repository.

## Deployment

The application can be prepared for deployment to a suitable hosting platform that supports Python/Django and PostgreSQL. A production deployment requires environment configuration, database provisioning, static-file handling, HTTPS, and a production application server.

No public deployment URL is provided in this README. Add one only after a deployment has been completed and verified.

## Future Improvements

Potential enhancements include:

- Automated unit and integration tests
- Production deployment and monitoring
- Improved chatbot intent recognition and error handling
- More detailed inventory reports and analytics
- Docker-based development and deployment workflow, if not yet implemented

## Author

**Shivangi Biswas**

GitHub: [shivangi-bis](https://github.com/shivangi-bis)
