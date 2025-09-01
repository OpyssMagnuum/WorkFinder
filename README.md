# A fastapi project i trained on
- Shows an API that works with DB
- Stack: **FastAPI**, **SQLAlchemy**, **Pydantic**, **PostgreSQL**, Alembic, Uvicorn, Typing
- You can simply launch app from main.py to run on a local server

##  Things to do better next time:
1. Had issues with relationships, should think through before project even more
2. All schemas are in one file, aren't really related, should be in different corresponding files
3. Find ways to implement more DRY in code, too tired of connecting to session in repository. Perhaps a decorator might do the job
4. Make prettier preview of what will come out after request, should be easy enough