# ReviewMate

### AI-Powered GitHub Pull Request Review Platform

ReviewMate is a full-stack application that automatically analyzes GitHub pull requests using AI and provides actionable code-review feedback. It combines GitHub integration, FastAPI, PostgreSQL, Redis/RQ, Gemini AI, and React into a complete local development workflow.

---

## Overview

Code reviews can be time-consuming, especially when developers need to manually inspect every pull request for potential issues, risks, and missing tests.

ReviewMate automates the first level of review by:

- Connecting GitHub repositories
- Receiving pull request events through GitHub Webhooks
- Fetching changed files from pull requests
- Sending code changes to Gemini AI for analysis
- Generating a structured review
- Assigning a risk level
- Providing recommendations
- Identifying whether tests may be missing
- Automatically posting the review back to the GitHub pull request

The project also uses Redis and RQ for background processing so that AI analysis can run asynchronously instead of blocking the API request.

---

## Key Features

### 🔐 GitHub OAuth Authentication

- GitHub OAuth login
- Secure user authentication
- JWT-based authorization
- Protected API endpoints

### 📦 Repository Management

- Synchronize repositories from GitHub
- View connected repositories
- Connect repositories to ReviewMate
- Disconnect repositories

### 🔔 GitHub Webhooks

- Receives GitHub repository events
- Handles pull request events
- Verifies webhook requests using HMAC SHA-256 signatures
- Stores webhook events for processing and tracking

### 🤖 AI-Powered Code Review

- Fetches changed files from GitHub pull requests
- Extracts code patches
- Sends changes to Gemini AI
- Generates structured review feedback
- Produces a risk score
- Provides recommendations
- Checks for missing tests
- Posts the generated review back to GitHub

### ⚡ Background Processing

- Redis used as the message broker
- RQ used for background job processing
- Pull request analysis runs through a worker
- Analysis status is tracked in the database

### 🗄️ Database

- PostgreSQL for persistent application data
- SQLAlchemy ORM
- Alembic migrations

### 🐳 Docker

- Backend containerization
- PostgreSQL container
- Redis container
- Background worker container
- Consistent local development environment
---

## How It Works

```text
                    ┌─────────────────────┐
                    │       GitHub        │
                    │  Repository / PR    │
                    └──────────┬──────────┘
                               │
                        Pull Request Event
                               │
                               ▼
                    ┌─────────────────────┐
                    │   GitHub Webhook    │
                    │ HMAC Verification   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │      Backend        │
                    └──────────┬──────────┘
                               │
                         Queue Job
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Redis + RQ      │
                    │   Background Queue  │
                    └──────────┬──────────┘
                               │
                         Worker picks job
                               │
                               ▼
                    ┌─────────────────────┐
                    │   GitHub Client     │
                    │ Fetch PR changes    │
                    └──────────┬──────────┘
                               │
                          Code Patch
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Gemini AI       │
                    │   Code Analysis     │
                    └──────────┬──────────┘
                               │
                        Review Result
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
          ┌──────────────────┐   ┌──────────────────┐
          │   PostgreSQL     │   │      GitHub      │
          │ Store Analysis   │   │ Post PR Comment  │
          └──────────────────┘   └──────────────────┘
---

## Tech Stack

### Backend
- Python
- FastAPI

### Database
- PostgreSQL
- SQLAlchemy
- Alembic

### Authentication
- GitHub OAuth
- JWT

### Background Processing
- Redis
- RQ

### AI
- Google Gemini API

### Frontend
- React

### Infrastructure
- Docker
- Docker Compose

### Version Control
- Git
- GitHub
---

## Running Locally

### Prerequisites

Make sure you have:

- Python 3.10+
- Node.js and npm
- Docker Desktop
- GitHub account
- GitHub OAuth application
- Gemini API key

### 1. Clone the Repository

From your terminal:

```bash
git clone https://github.com/srigayatrii/reviewmate.git
cd reviewmate
```

### 2. Configure Environment Variables

Create a `.env` file with the required configuration:

```env
DATABASE_URL=your_database_url

GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

GITHUB_WEBHOOK_SECRET=your_webhook_secret

GEMINI_API_KEY=your_gemini_api_key

JWT_SECRET_KEY=your_jwt_secret
```

Do not commit the `.env` file or expose API keys and secrets.

### 3. Start the Backend Services

From the project root:

```bash
docker compose up -d
```

This starts:

* FastAPI backend
* PostgreSQL
* Redis
* RQ worker

### 4. Start the Frontend

From the `frontend` directory:

```bash
npm install
npm run dev
```

### 5. API Documentation

FastAPI Swagger documentation is available at:

```text
http://localhost:8000/docs
```
---

## AI Review Output

ReviewMate analyzes pull request changes and generates:

- Summary
- Risk score
- Recommendations
- Missing test indication
- Description mismatch indication

The generated review is stored in PostgreSQL and posted back to the GitHub pull request.
---

## Security

ReviewMate uses:

- GitHub OAuth for authentication
- JWT-based authorization
- HMAC SHA-256 for GitHub webhook verification
- Environment variables for sensitive configuration

API keys and secrets are kept on the backend and are not exposed through the frontend.
