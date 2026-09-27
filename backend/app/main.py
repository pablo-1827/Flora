from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.routers.auth import router as auth_router
from app.routers.opportunities import router as opportunities_router
from app.routers.profile import router as profile_router

settings = get_settings()

app = FastAPI(
    title=settings.project_name,
    version="0.1.0",
    description="OpportunityHub backend API",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": settings.project_name, "environment": settings.environment}


app.include_router(auth_router, prefix=settings.api_v1_prefix)
app.include_router(profile_router, prefix=settings.api_v1_prefix)
app.include_router(opportunities_router, prefix=settings.api_v1_prefix)


@app.get("/")
def root():
    return {"message": "OpportunityHub API is running"}
