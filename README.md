# Aesstore

> **B2B E-commerce Platform** - Modern fullstack application for wholesale businesses

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Next.js: 14](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=postgresql)](https://www.postgresql.org/)

---

## 📋 Table of Contents

- [🚀 Features](#-features)
- [🏗️ Architecture](#-architecture)
- [📦 Tech Stack](#-tech-stack)
- [🚀 Quick Start](#-quick-start)
- [🛠️ Installation](#-installation)
  - [Prerequisites](#prerequisites)
  - [Development Setup](#development-setup)
  - [Docker Setup](#docker-setup)
- [📂 Project Structure](#-project-structure)
- [🎯 API Documentation](#-api-documentation)
- [🔧 Configuration](#-configuration)
- [🧪 Testing](#-testing)
- [📦 Build & Deployment](#-build--deployment)
- [🤖 CI/CD](#-cicd)
- [📜 License](#-license)
- [🤝 Contributing](#-contributing)
- [🙏 Acknowledgments](#-acknowledgments)

---

## 🚀 Features

### ✅ Core Features

- **Multi-tenant B2B Platform** - Support for vendors and customers
- **Product Management** - Full CRUD operations for products with categories, images, variants
- **Order Management** - Complete order lifecycle from creation to delivery
- **Shopping Cart** - Persistent cart with real-time updates
- **User Authentication** - JWT-based authentication with refresh tokens
- **Role-Based Access Control** - Admin, Vendor, and Customer roles
- **Search & Filtering** - Advanced product search with filters
- **API Documentation** - Automatic OpenAPI/Swagger documentation
- **Real-time Updates** - WebSocket support for live updates
- **File Uploads** - Product images and document uploads

### 🎨 UI Features

- **Modern Dashboard** - Analytics and statistics visualization
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Dark Mode** - Automatic dark/light theme switching
- **Accessibility** - WCAG 2.1 compliant
- **Internationalization** - Multi-language support (French, English)
- **Form Validation** - Client and server-side validation
- **Error Handling** - User-friendly error messages
- **Loading States** - Smooth transitions and loading indicators

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                              CLIENT                                    │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                    Next.js 14 Frontend                           │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐   │  │
│  │  │  Pages   │  │ Components│  │  Hooks   │  │   Stores    │   │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────────┘   │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                    │  │
│  │  │  Types   │  │  Utils   │  │ Services  │                    │  │
│  │  └──────────┘  └──────────┘  └──────────┘                    │  │
│  └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                         API GATEWAY (Nginx)                          │
└─────────────────────────────────────────────────────────────────┘
                                    │
              ┌─────────────────────┴─────────────────────┐
              │                                           │
              ▼                                           ▼
┌─────────────────────────┐             ┌─────────────────────────┐
│      FastAPI Backend      │             │      PostgreSQL           │
├─────────────────────────┤             ├─────────────────────────┤
│  ┌─────────────────────┐  │             │  - Primary Database       │
│  │   API Routers       │  │             │  - User Management        │
│  └─────────────────────┘  │             │  - Product Data          │
│  ┌─────────────────────┐  │             │  - Order History         │
│  │   Services          │  │             └─────────────────────────┘
│  └─────────────────────┘  │
│  ┌─────────────────────┐  │
│  │   Database Models    │  │
│  └─────────────────────┘  │
│  ┌─────────────────────┐  │
│  │   Authentication     │  │
│  └─────────────────────┘  │
└─────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                              CACHE                                   │
│                         Redis (Optional)                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Tech Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| [Python](https://www.python.org/) | 3.11+ | Primary Language |
| [FastAPI](https://fastapi.tiangolo.com/) | 0.109+ | Web Framework |
| [Uvicorn](https://www.uvicorn.org/) | 0.27+ | ASGI Server |
| [SQLAlchemy](https://www.sqlalchemy.org/) | 2.0+ | ORM |
| [AsyncPG](https://github.com/MagicStack/asyncpg) | 0.29+ | PostgreSQL Driver |
| [Alembic](https://alembic.sqlalchemy.org/) | 1.13+ | Database Migrations |
| [Pydantic](https://pydantic.dev/) | 2.5+ | Data Validation |
| [JWT](https://jwt.io/) | PyJWT | Authentication |
| [Passlib](https://passlib.readthedocs.io/) | 1.7+ | Password Hashing |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| [Next.js](https://nextjs.org/) | 14.0+ | React Framework |
| [React](https://react.dev/) | 18.2+ | UI Library |
| [TypeScript](https://www.typescriptlang.org/) | 5.3+ | Type Safety |
| [Tailwind CSS](https://tailwindcss.com/) | 3.4+ | Styling |
| [Radix UI](https://www.radix-ui.com/) | 2.0+ | Headless Components |
| [TanStack Query](https://tanstack.com/query/latest) | 5.0+ | Data Fetching |
| [Zustand](https://github.com/pmndrs/zustand) | 4.4+ | State Management |
| [Zod](https://zod.dev/) | 3.22+ | Schema Validation |
| [React Hook Form](https://react-hook-form.com/) | 7.49+ | Form Management |
| [Framer Motion](https://www.framer.com/motion/) | 11.0+ | Animations |
| [Lucide React](https://lucide.dev/) | 0.309+ | Icons |

### Infrastructure

| Technology | Version | Purpose |
|------------|---------|---------|
| [Docker](https://www.docker.com/) | 24+ | Containerization |
| [Docker Compose](https://docs.docker.com/compose/) | 2.23+ | Multi-container Orchestration |
| [PostgreSQL](https://www.postgresql.org/) | 15+ | Database |
| [Redis](https://redis.io/) | 7+ | Caching |
| [Nginx](https://www.nginx.com/) | Latest | Reverse Proxy |
| [GitHub Actions](https://github.com/features/actions) | - | CI/CD |

---

## 🚀 Quick Start

The fastest way to get started with Aesstore:

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/julienDALLA/Aesstore-.git
cd Aesstore-

# Start all services with Docker Compose
make up

# Or manually:
docker-compose up -d
```

Then open:
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000
- **PGAdmin**: http://localhost:5050 (admin@aesstore.com / admin123)
- **MailHog**: http://localhost:8025

### Local Development

```bash
# Clone the repository
git clone https://github.com/julienDALLA/Aesstore-.git
cd Aesstore-

# Install dependencies
make install

# Start development servers
make dev
```

---

## 🛠️ Installation

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python** 3.11 or higher
- **Node.js** 18 or higher
- **Docker** 24 or higher (optional, for containerized development)
- **Docker Compose** 2.23 or higher (optional)
- **PostgreSQL** 15 or higher (if not using Docker)
- **Git** 2.30 or higher

#### Verify Installation

```bash
# Check Python version
python --version

# Check Node.js version
node --version

# Check npm version
npm --version

# Check Docker version
docker --version

# Check Docker Compose version
docker-compose --version
```

### Development Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/julienDALLA/Aesstore-.git
cd Aesstore-
```

#### 2. Create Virtual Environment (Backend)

```bash
# Create virtual environment
python -m venv .venv

# Activate on Linux/macOS
source .venv/bin/activate

# Activate on Windows
.\.venv\Scripts\activate
```

#### 3. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
cd ..
```

#### 4. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

#### 5. Configure Environment Variables

Copy the example environment files:

```bash
# Backend
cp backend/.env.example backend/.env

# Frontend
cp frontend/.env.example frontend/.env.local
```

Edit the files to match your configuration:

**backend/.env:**
```ini
APP_NAME=Aesstore API
APP_VERSION=1.0.0
APP_DESCRIPTION=B2B E-commerce Platform Backend
DEBUG=True

# Server
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/aesstore

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**frontend/.env.local:**
```ini
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Aesstore
NEXT_PUBLIC_APP_VERSION=1.0.0
```

#### 6. Initialize Database

```bash
# Create database (if not using Docker)
createdb aesstore

# Run migrations
cd backend
alembic upgrade head
cd ..
```

#### 7. Start Development Servers

In separate terminals:

```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

Or use the Makefile:

```bash
make dev
```

### Docker Setup

#### 1. Build and Start Containers

```bash
# Build and start all services
docker-compose up -d --build

# View running containers
docker-compose ps
```

#### 2. Initialize Database

The database will be automatically initialized when the containers start.

#### 3. Access Services

- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000
- **PGAdmin**: http://localhost:5050
- **MailHog**: http://localhost:8025

#### 4. Stop Services

```bash
# Stop all containers
docker-compose down

# Stop and remove all containers, networks, and volumes
docker-compose down -v
```

---

## 📂 Project Structure

```
aesstore/
├── backend/                          # Backend API
│   ├── app/                         # Application source
│   │   ├── api/                     # API routers and endpoints
│   │   │   └── v1/                  # API version 1
│   │   │       └── endpoints/      # Endpoint modules
│   │   ├── core/                    # Core utilities and config
│   │   ├── database/                # Database models and session
│   │   │   ├── models.py           # SQLAlchemy models
│   │   │   ├── session.py          # Database session management
│   │   │   └── base.py             # Base model
│   │   ├── schemas/                 # Pydantic schemas
│   │   └── main.py                 # FastAPI application entry
│   ├── tests/                       # Tests
│   ├── requirements.txt             # Python dependencies
│   ├── pyproject.toml              # Python project config
│   └── .env.example                # Environment example
│
├── frontend/                        # Frontend Application
│   ├── src/                        # Source code
│   │   ├── app/                    # Next.js app router
│   │   │   ├── (auth)/             # Auth pages (login, register)
│   │   │   └── dashboard/          # Dashboard pages
│   │   ├── components/             # React components
│   │   │   ├── ui/                # UI components (shadcn/ui)
│   │   │   └── layout/            # Layout components
│   │   ├── lib/                     # Utilities and constants
│   │   ├── services/               # API services
│   │   ├── stores/                 # Zustand stores
│   │   ├── types/                  # TypeScript types
│   │   └── styles/                 # Global styles
│   ├── public/                     # Static files
│   ├── package.json                # Node dependencies
│   ├── tsconfig.json               # TypeScript config
│   ├── tailwind.config.ts          # Tailwind config
│   └── next.config.js              # Next.js config
│
├── docker-compose.yml              # Docker Compose (dev)
├── docker-compose.prod.yml         # Docker Compose (production)
├── Dockerfile                      # Production Dockerfile
├── Dockerfile.dev                 # Development Dockerfile
├── .dockerignore                   # Docker ignore file
├── Makefile                        # Makefile for common tasks
├── .github/                        # GitHub configuration
│   ├── workflows/                  # CI/CD workflows
│   ├── ISSUE_TEMPLATE/             # Issue templates
│   ├── PULL_REQUEST_TEMPLATE.md    # PR template
│   └── dependabot.yml              # Dependabot config
└── README.md                       # This file
```

---

## 🎯 API Documentation

The API is automatically documented using FastAPI and OpenAPI.

### Access API Docs

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### API Endpoints

#### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/login` | Login user |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| POST | `/api/v1/auth/logout` | Logout user |
| POST | `/api/v1/auth/forgot-password` | Request password reset |
| POST | `/api/v1/auth/reset-password` | Reset password |
| POST | `/api/v1/auth/change-password` | Change password |
| GET | `/api/v1/auth/me` | Get current user |

#### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/users` | List all users |
| POST | `/api/v1/users` | Create a user |
| GET | `/api/v1/users/{id}` | Get user by ID |
| PUT | `/api/v1/users/{id}` | Update user |
| DELETE | `/api/v1/users/{id}` | Delete user |

#### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/products` | List all products |
| POST | `/api/v1/products` | Create a product |
| GET | `/api/v1/products/{slug}` | Get product by slug |
| PUT | `/api/v1/products/{id}` | Update product |
| DELETE | `/api/v1/products/{id}` | Delete product |
| GET | `/api/v1/products/search` | Search products |
| GET | `/api/v1/products/featured` | Get featured products |
| GET | `/api/v1/products/category/{slug}` | Get products by category |

#### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/categories` | List all categories |
| POST | `/api/v1/categories` | Create a category |
| GET | `/api/v1/categories/{slug}` | Get category by slug |
| PUT | `/api/v1/categories/{id}` | Update category |
| DELETE | `/api/v1/categories/{id}` | Delete category |
| GET | `/api/v1/categories/tree` | Get category tree |

#### Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/orders` | List all orders |
| POST | `/api/v1/orders` | Create an order |
| GET | `/api/v1/orders/{order_number}` | Get order by number |
| PUT | `/api/v1/orders/{id}` | Update order |
| GET | `/api/v1/orders/my` | Get my orders |
| GET | `/api/v1/orders/vendor` | Get vendor orders |

#### Cart

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/cart` | Get cart |
| POST | `/api/v1/cart/items` | Add item to cart |
| PUT | `/api/v1/cart/items/{id}` | Update cart item |
| DELETE | `/api/v1/cart/items/{id}` | Remove item from cart |
| POST | `/api/v1/cart/clear` | Clear cart |
| POST | `/api/v1/cart/checkout` | Checkout |

#### Reviews

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/reviews/product/{slug}` | Get product reviews |
| POST | `/api/v1/reviews` | Create a review |
| PUT | `/api/v1/reviews/{id}` | Update review |
| DELETE | `/api/v1/reviews/{id}` | Delete review |
| GET | `/api/v1/reviews/my` | Get my reviews |

#### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/health/ready` | Readiness check |
| GET | `/api/v1/health/live` | Liveness check |

---

## 🔧 Configuration

### Environment Variables

#### Backend

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | Aesstore API |
| `APP_VERSION` | Application version | 1.0.0 |
| `APP_DESCRIPTION` | Application description | B2B E-commerce Platform Backend |
| `DEBUG` | Debug mode | False |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8000 |
| `DATABASE_URL` | Database connection URL | postgresql+asyncpg://user:password@db:5432/aesstore |
| `SECRET_KEY` | JWT secret key | - |
| `ALGORITHM` | JWT algorithm | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiration | 30 |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token expiration | 7 |
| `CORS_ORIGINS` | Allowed CORS origins | http://localhost:3000 |
| `LOG_LEVEL` | Logging level | INFO |

#### Frontend

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | API base URL | http://localhost:8000 |
| `NEXT_PUBLIC_APP_NAME` | Application name | Aesstore |
| `NEXT_PUBLIC_APP_VERSION` | Application version | 1.0.0 |

### Database Configuration

The application uses PostgreSQL as the primary database. Connection is configured via the `DATABASE_URL` environment variable.

#### Connection URL Format

```
postgresql+asyncpg://username:password@host:port/database
```

#### Example for Docker

```
postgresql+asyncpg://user:password@db:5432/aesstore
```

#### Example for Local Development

```
postgresql+asyncpg://user:password@localhost:5432/aesstore
```

---

## 🧪 Testing

### Backend Tests

```bash
# Run all tests
cd backend
python -m pytest tests/ --asyncio-mode=auto -v

# Run tests with coverage
python -m pytest tests/ --asyncio-mode=auto --cov=app --cov-report=html

# Run specific test file
python -m pytest tests/test_auth.py -v

# Run with verbose output
python -m pytest tests/ -v -s
```

### Frontend Tests

```bash
# Run all tests
cd frontend
npm test

# Run tests with coverage
npm run test:coverage

# Run tests with UI
npm run test:ui
```

### Test Files Structure

```
backend/tests/
├── conftest.py              # Pytest fixtures
├── test_auth.py             # Authentication tests
├── test_users.py            # User tests
├── test_products.py         # Product tests
├── test_categories.py       # Category tests
├── test_orders.py           # Order tests
├── test_cart.py             # Cart tests
└── test_reviews.py          # Review tests
```

---

## 📦 Build & Deployment

### Development Build

```bash
# Build backend
cd backend
pip install -r requirements.txt

# Build frontend
cd frontend
npm install
npm run build
```

### Production Build

```bash
# Build Docker images
docker-compose -f docker-compose.prod.yml build

# Start production services
docker-compose -f docker-compose.prod.yml up -d

# Stop production services
docker-compose -f docker-compose.prod.yml down
```

### Docker Commands

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend

# Execute command in container
docker-compose exec backend bash

# Clean up
docker system prune -a -f --volumes
```

### Deployment to Production

1. **Configure environment variables** in `.env` and `docker-compose.prod.yml`
2. **Set up SSL certificates** for Nginx (optional)
3. **Configure domain** and DNS settings
4. **Run production build**:

```bash
# Build and deploy
make prod-build
make prod-up
```

5. **Verify deployment**:

```bash
# Check health endpoint
curl http://your-domain.com/api/v1/health
```

---

## 🤖 CI/CD

The project uses GitHub Actions for Continuous Integration and Deployment.

### Workflows

| Workflow | Trigger | Description |
|----------|---------|-------------|
| `ci.yml` | Push to main/develop | Run tests and linters |
| `cd.yml` | Push to main | Deploy to production |
| `docs.yml` | Push to main/develop | Build and deploy documentation |

### CI Pipeline

1. **Test Stage**: Runs unit tests for both backend and frontend
2. **Lint Stage**: Checks code style and formatting
3. **Build Stage**: Builds Docker images
4. **Security Stage**: Scans for vulnerabilities

### CD Pipeline

1. **Build**: Builds production Docker images
2. **Push**: Pushes images to container registry
3. **Deploy**: Deploys to production server via SSH
4. **Verify**: Checks deployment health
5. **Notify**: Sends notifications to Slack/Discord

### Environment Secrets

Required GitHub Secrets for CI/CD:

- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub password
- `SSH_PRIVATE_KEY` - SSH private key for server
- `SSH_KNOWN_HOSTS` - SSH known hosts
- `SSH_USERNAME` - SSH username
- `SSH_HOST` - SSH host
- `APP_URL` - Application URL
- `SLACK_WEBHOOK` - Slack webhook URL (optional)
- `DISCORD_WEBHOOK` - Discord webhook URL (optional)
- `CODECOV_TOKEN` - Codecov token (optional)

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Aesstore

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linters
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Pull Request Guidelines

- Follow the [Pull Request Template](.github/PULL_REQUEST_TEMPLATE.md)
- Include tests for new features
- Update documentation as needed
- Keep commits atomic and well-described
- Reference any related issues

### Code Style

- **Python**: Follow PEP 8 guidelines
- **TypeScript**: Follow TypeScript best practices
- **Formatting**: Use Black (Python) and Prettier (TypeScript)
- **Linting**: Use flake8 (Python) and ESLint (TypeScript)

### Commit Message Format

```
type(scope): description

body

footer
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `build`, `ci`, `revert`

Example:
```
feat(auth): add JWT token refresh

- Implement token refresh endpoint
- Add refresh token storage
- Update auth middleware

Closes #123
```

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Web framework for building APIs
- [Next.js](https://nextjs.org/) - React framework for production
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
- [Radix UI](https://www.radix-ui.com/) - Headless UI components
- [TanStack Query](https://tanstack.com/query/latest) - Data fetching library
- [Zustand](https://github.com/pmndrs/zustand) - State management library
- [shadcn/ui](https://ui.shadcn.com/) - Beautiful UI components

---

## 📞 Support

- **Documentation**: [https://docs.aesstore.com](https://docs.aesstore.com) (coming soon)
- **Issues**: [GitHub Issues](https://github.com/julienDALLA/Aesstore-/issues)
- **Discussions**: [GitHub Discussions](https://github.com/julienDALLA/Aesstore-/discussions)
- **Email**: support@aesstore.com (coming soon)

---

**Made with ❤️ by [julienDALLA](https://github.com/julienDALLA)**

*Last updated: January 2025*
