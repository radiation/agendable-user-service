# Agendable

## Overview

Agendable is a microservices application for managing meetings and users:

- **User Service**: FastAPI app for user authentication, profiles, and preferences
- **Meeting Service**: FastAPI app for meeting and task management
- **Notification Service**: FastAPI app for alerts and user communications
- **Web UI**: Vite / Typescript app for primary usage
- **Admin Console**: Vite / Typescript app for system management and admin
- **Celery**: Responsible for asynchronous task management
- **Kong Gateway**: API gateway to manage routing and security
- **PostgreSQL**: Database service
- **Redis**: Supports caching needs

The app is containerized using Docker and orchestrated with `docker-compose`.

---

## File Structure

```plaintext
.
├── docker-compose.yml
├── .env                   # Environment variable configuration
├── init-db.sh             # Database initialization script
├── user-service/
│   ├── app/
│   │   ├── main.py         # FastAPI app entry point for User Service
│   │   ├── db/             # Database models & repositories
│   │   ├── routers/        # API route definitions
│   │   └── core/           # Core utilities (decorators, helpers, etc.)
│   └── Dockerfile          # Dockerfile for building User Service
├── meeting-service/
│   ├── app/
│   │   ├── main.py         # FastAPI app entry point for Meeting Service
│   │   ├── db/             # Database models & repositories
│   │   ├── routers/        # API route definitions
│   │   └── core/           # Core utilities
│   └── Dockerfile          # Dockerfile for building Meeting Service
├── kong/
│   ├── kong.conf           # Kong configuration
│   └── Dockerfile          # Dockerfile for Kong Gateway
└── README.md               # Project documentation
```

---

## Prerequisites

Ensure the following are installed on your machine:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- `make` (optional, for simplifying commands)

---

## Environment Variables

### Example `.env` File

```plaintext
# Logging
LOG_LEVEL=DEBUG

# Google OAuth2 credentials
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback

# Secret key for token generation
SECRET_KEY=your_secret_key_for_token_generation

# Postgres
POSTGRES_PORT=5432
POSTGRES_USER=user
POSTGRES_PASSWORD=password

# User Service
USER_SERVICE_PORT=8004
USER_SERVICE_URL=http://localhost:${USER_SERVICE_PORT}
USER_DB_URL=postgresql+asyncpg://user:password@postgres/user_db

# Meeting Service
MEETING_SERVICE_PORT=8005
MEETING_SERVICE_URL=http://localhost:${MEETING_SERVICE_PORT}
MEETING_DB_URL=postgresql+asyncpg://user:password@postgres/meeting_db

# Kong
KONG_PROXY_PORT=8000
KONG_PROXY_SSL_PORT=8443
KONG_ADMIN_PORT=8001
KONG_URL=http://localhost:${KONG_ADMIN_PORT}

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
```

---

## Building and Running the Application

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/radiation/agendable.git
   cd agendable
   ```

2. **Configure Environment Variables**:
   Copy the `.env` file and fill in the required values:
   ```bash
   cp .env.example .env
   ```

3. **Start the Application**:
   ```bash
   docker-compose up --build
   ```

4. **Access Services**:
   - User Service: [http://localhost:8004](http://localhost:8004)
   - Meeting Service: [http://localhost:8005](http://localhost:8005)
   - Kong Admin: [http://localhost:8001](http://localhost:8001)
   - Kong Proxy: [http://localhost:8000](http://localhost:8000)

---

## Services

### User Service
- FastAPI-based backend for managing users.
- Includes authentication and user profile endpoints.

### Meeting Service
- FastAPI-based backend for meeting management.
- Features task and agenda management.

### Notification Service
- FastAPI-based backend for notifications.

### Celery
- Asynchronous task management system.

### Kong Gateway
- API gateway for routing requests to respective services.

### PostgreSQL
- Database service for storing user and meeting data.
- Includes initialization scripts for creating default schemas.

### Redis
- Provides caching for improved performance.

---

## Troubleshooting

- **Database Connection Issues**:
  Ensure that the `DATABASE_URL` values in the `.env` file match your `docker-compose` configuration.

- **Container Health Checks**:
  Use the following command to inspect container statuses:
  ```bash
  docker-compose ps
  ```

---

## Contributing

Contributions are welcome! Submit a pull request or open an issue for suggestions and fixes.

---
