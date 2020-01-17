An over-engineered back-end for a Monster Hunter World monsters API

Uses

- FastAPI
- SQLite / SQLAlchemy

Requires:

- Python 3.8

Setup:

- `pip install --upgrade poetry`
- `poetry install`
- `uvicorn main:app --reload`

API docs available at `localhost:8000/docs`

WIP:

- Need a database setup
- Image sourcing
- GET wired
- PUT/POST wired
- Converts to and from SQLite
- Remove extra code
- Write tests
- Convert to PSQL
- Dockerize
- Deploy
- Keep over-engineering to learn
