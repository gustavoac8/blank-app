from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version='1.0.0')
app.include_router(router)


@app.get('/health')
def health():
    return {'status': 'ok'}
