# Reward Decision Service

A low-latency, deterministic Reward Decision microservice built using **FastAPI**.
The service evaluates reward outcomes for transactions using **config-driven policies**
and a **cache-first architecture** with Redis and in-memory fallback.

This project is designed to demonstrate backend engineering fundamentals:
scalability, correctness, clean architecture (SOLID), and performance discipline.

---

## 🚀 Features

- FastAPI-based backend service
- Deterministic reward decision logic
- Idempotent request handling
- Config-driven policy evaluation (YAML)
- Redis-first caching with in-memory fallback
- Persona-based reward calculation
- Daily CAC cap enforcement
- No database in hot path
- Unit tests using pytest
- Simple async load testing (~300 RPS)

---

## 🧱 Architecture Overview

Client
↓
FastAPI (API Layer)
↓
RewardService (Business Logic – SOLID)
↓
Cache Abstraction
├── Redis (primary)
└── In-Memory (fallback)
↓
Policy Configuration (YAML)


### Design Principles
- **SOLID**
- **Dependency Inversion**
- **Cache-first**
- **Deterministic & Idempotent**
- **Low-latency focused**


## 📦 Tech Stack

- Python 3.10+
- FastAPI
- Redis (optional but recommended)
- Pydantic
- PyYAML
- httpx
- pytest


## 📂 Project Structure

app/
├── api/ # API routes
├── cache/ # Cache abstraction & implementations
├── config/ # Policy configuration
├── models/ # Request / Response schemas
├── services/ # Business logic
├── utils/ # Helpers
└── main.py # Application entry point

tests/
└── test_reward_service.py

loadtest/
└── load_test.py


## API Contract

### POST `/reward/decide`

#### Request
{
  "txn_id": "string",
  "user_id": "string",
  "merchant_id": "string",
  "amount": 100,
  "txn_type": "PAY",
  "ts": "2024-01-01T00:00:00"
}


#### Response
{
  "decision_id": "uuid",
  "policy_version": "v1",
  "reward_type": "XP",
  "reward_value": 0,
  "xp": 150,
  "reason_codes": [],
  "meta": {
    "persona": "NEW"
  }
}

## Setup & Running the Service

Prerequisites

Python 3.10+

Redis (optional but recommended)

pip / virtualenv


### Clone the Repository
git clone <your-github-repo-url>
cd reward-decision-service


### Create Virtual Environment
python -m venv venv
source venv/bin/activate
venv\Scripts\activate


### Install Dependencies
pip install -r requirements.txt


### Environment Variables
Create a .env file in the root directory:
REDIS_URL=redis://localhost:6379


### Start the Application
uvicorn app.main:app --reload


### API Endpoint
POST /reward/decide


### Run Tests
pytest


### Simple Load Test (Async)
python load_test.py