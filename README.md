# AgentOS

AgentOS is the web-developer foundation for a personal AI operating system. It provides the essential infrastructure, authentication, data layer, and the dashboard UI shell. The actual AI/ML integration—including the LangGraph ReAct loop, ChromaDB embeddings, prompt engineering, and tool execution—is designed to plug seamlessly into this foundation via isolated integration seams.

## 🚀 Key Features

*   **Robust Authentication**: JWT-based authentication via PyJWT with secure Argon2 password hashing. Features include registration, login, token refresh, and protected endpoints. Designed with SOLID principles, making OAuth integration trivial.
*   **Production-Ready Database**: SQLAlchemy 2.0 with asynchronous PostgreSQL support (`asyncpg`). Fully integrated with Alembic for robust schema migrations and designed out-of-the-box to work with Neon serverless Postgres.
*   **High-Performance API**: Built on FastAPI and Python 3.11 for incredible speed and native async support. Includes custom routing, error handling, rate limiting, and dependency injection.
*   **Modern Frontend Stack**: A sleek, responsive dashboard built with React, Vite, and Tailwind CSS v4. Features a custom design system mimicking a system UI with pre-built mock components (`ChatPanel`, `ToolStatus`, `TaskBoard`, `MemoryViewer`).
*   **Extensible Architecture**: Chat endpoints are pre-configured to stream responses via Server-Sent Events (SSE), awaiting your LangGraph/LLM logic to start yielding tokens.

---

## 🛠️ Tech Stack

### Frontend
*   **Framework**: React (Vite)
*   **Language**: TypeScript
*   **Styling**: Tailwind CSS v4 (Vanilla CSS variables for theming)

### Backend
*   **Framework**: FastAPI, Uvicorn
*   **Language**: Python 3.11+
*   **Database ORM**: SQLAlchemy 2.0 (Async)
*   **Database Migrations**: Alembic
*   **Caching / Sessions**: Redis (asyncio)
*   **Authentication**: PyJWT, Argon2, Passlib
*   **Background Jobs**: APScheduler

---

## 🏗️ Getting Started (Local Development)

### 1. Prerequisites
Ensure you have the following installed:
*   [Node.js](https://nodejs.org/) & [pnpm](https://pnpm.io/)
*   [Python 3.11+](https://www.python.org/)
*   [Docker](https://www.docker.com/) & Docker Compose (optional for local DB/Redis)
*   A serverless Postgres account (like [Neon](https://neon.tech/)) and an Upstash Redis account (recommended for cloud sync).

### 2. Environment Configuration

Clone the repository and set up your environment variables.

**Backend (`backend/.env`):**
```bash
cp backend/.env.example backend/.env
```
Ensure your `DATABASE_URL` is set to your Neon DB connection string. **Important:** Change the scheme to `postgresql+asyncpg://` and append `?ssl=require`.
Example:
```env
DATABASE_URL="postgresql+asyncpg://<user>:<password>@<host>/<dbname>?ssl=require"
REDIS_URL="rediss://default:<password>@<host>:<port>"
```

**Frontend (`frontend/.env`):**
```bash
cp frontend/.env.example frontend/.env
```

### 3. Backend Setup

It is highly recommended to run the backend in a virtual environment.

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

*(Note: Before deploying or updating dependencies, it's good practice to clear cached files: `Get-ChildItem -Path . -Include __pycache__ -Recurse -Directory -Force | Remove-Item -Recurse -Force` on Windows).*

### 4. Database Initialization (Alembic)

Once your `.env` is configured with your external DB, generate and apply the migrations to create your tables (like the `users` table).

```powershell
cd backend
# Only run autogenerate if you are creating new models/tables
alembic revision --autogenerate -m "Initial migration"

# Apply migrations to the database
alembic upgrade head
```

### 5. Running the Application

**Run the Backend API:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```
The API documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

**Run the Frontend Development Server:**
```powershell
cd frontend
pnpm install
pnpm run dev
```
The frontend will be available at [http://localhost:5173](http://localhost:5173).

---

## 📂 Project Structure

### `/backend`
*   `app/api/v1/routes/`: Contains all FastAPI endpoints (`auth.py`, `users.py`, `health.py`, `chat.py`).
*   `app/core/`: Security configs, exceptions, and settings definitions.
*   `app/db/`: SQLAlchemy models and async session configuration.
*   `app/repositories/`: Data access layer abstracting direct DB queries (e.g., `user_repository.py`).
*   `app/services/`: Business logic layer (e.g., `user_service.py`).
*   `alembic/`: Database migration scripts.

### `/frontend`
*   `src/components/`: Reusable UI components.
*   `src/layouts/`: The main AppShell wrapping the dashboard.
*   `src/pages/`: Main views (Landing, Auth, Dashboard).
*   `src/hooks/`: Custom React hooks (e.g., `useAuth`).
*   `src/index.css`: Tailwind configuration and core design system CSS variables.

---

## 🔒 Authentication Flow
The application uses a highly abstracted Auth flow. Currently, it uses a `JWTAuthProvider`. The abstraction (`AuthProviderProtocol`) ensures that if you decide to implement OAuth later, you only need to create a new provider class without touching the core routing logic—strictly following the **Open/Closed Principle**.

---

## 🤖 Next Steps: Integrating the AI
The frontend is already configured to read Server-Sent Events (SSE) from the backend's `/api/v1/chat` endpoint. 

Currently, `chat.py` is configured as an `AsyncGenerator` yielding a placeholder string. To plug in your AI:
1. Initialize your LangGraph agents in the backend.
2. Modify `run_agent_reasoning_loop()` in `chat.py` to `yield` tokens dynamically as the LLM generates them.

---

## 🧪 Testing
The backend features an asynchronous Pytest suite testing the registration, authentication, and dependency injection layers.

```bash
cd backend
pytest -v
```
