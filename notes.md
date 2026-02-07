
create project in fast api

1️⃣ Create virtual environment (recommended)
    run cmd - $ python3 -m venv myvenv => to create virtual environment
    on Mac/Linux
    run cmd - $ source myvenv/bin/activate => to activate venv
    on Windows
    venv\Scripts\activate

2️⃣ Install FastAPI & server
    pip install fastapi uvicorn

▶️ Step 3: Run the server
    uvicorn app.main:app --reload

    here uvicorn is server
         app.main is module name
         app is  fast api instance
        --reload → auto restart (dev mode)


Once running, you can:
Visit: http://127.0.0.1:8000/health (your health endpoint)
Visit: http://127.0.0.1:8000/docs (automatic interactive API docs)
Visit: http://127.0.0.1:8000/redoc (alternative API documentation)








backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app instance & startup
│   ├── config.py               # Configuration (Pydantic BaseSettings)
│   ├── dependencies.py         # Shared dependencies
│   │
│   ├── api/                    # API layer
│   │   ├── __init__.py
│   │   └── v1/                 # API versioning
│   │       ├── __init__.py
│   │       └── endpoints/      # Route handlers
│   │           ├── __init__.py
│   │           ├── auth.py
│   │           ├── users.py
│   │           └── items.py
│   │
│   ├── core/                   # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py           # Settings
│   │   ├── security.py         # Authentication/authorization
│   │   └── database.py         # DB connection
│   │
│   ├── models/                 # SQLAlchemy/Pydantic models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   │
│   ├── schemas/                # Pydantic schemas (request/response)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   │
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   │
│   ├── repositories/           # Data access layer (optional)
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   └── item_repository.py
│   │
│   └── utils/                  # Utilities
│       ├── __init__.py
│       └── helpers.py
│
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
│
├── tests/                      # Tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api/
│   └── test_services/
│
├── .env                        # Environment variables
├── .env.example
├── requirements.txt            # Dependencies
├── pyproject.toml              # Project config (optional)
└── README.md