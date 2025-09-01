from fastapi import Depends
from src.database import get_async_session

a_session_dep = Depends(get_async_session)
