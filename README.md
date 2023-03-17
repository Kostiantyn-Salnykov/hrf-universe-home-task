Start back-end:

`cp .env.example .env`

(new Docker compose version)
```commandline
docker compose up -d
```

(old Docker compose version)
```commandline
docker-compose up -d
```

Back-end will be started at: `0.0.0.0:8000`

[Docs here](http://0.0.0.0:8000/docs)

Run CLI:
```commandline
poetry run python cli.py
```


Structure:
- deps.py (FastAPI Dependencies)
- enums.py (Enums and Status codes)
- exceptions (Custom Exceptions for API and FastAPI)
- handlers (FastAPI handlers)
- routers (FastAPI Routers), but business logic should be in `handlers.py`, `services.py` (simplified for this task)
- schemas (Pydantic's BaseModel classes to In/Out logic)
- types (Pydantic's types to In/Out validations)
- main.py (instance of FastAPI app, entry point)
- Makefile (Useful commands)
