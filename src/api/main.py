from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(title="Customer Support AI API")

# Include routes
app.include_router(router)

@app.get("/")
def home():
    return {"message": "API is running successfully"}