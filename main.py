from fastapi import FastAPI
import logging
from app.infrastructure.api.routes import router
from app.infrastructure.config.database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

app = FastAPI(title="P12 to POM Converter API")

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing application...")
    await init_db()
    logger.info("Database initialized")

app.include_router(router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)