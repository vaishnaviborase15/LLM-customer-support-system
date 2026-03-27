from fastapi import FastAPI
from src.api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Customer Support AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

@app.get("/")
def home():
    return {"message": "API is running successfully"}


@app.get("/health")
def health():
    return {"status": "running"}