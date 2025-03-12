from fastapi import FastAPI

from convert_certificates.routes import certificate_routes

app = FastAPI()
app.include_router(certificate_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
