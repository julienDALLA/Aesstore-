"""
Health check endpoint.
"""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.core.dependencies import HealthCheckResponse
from app.core.config import settings


router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", summary="Health Check", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        HealthCheckResponse: Current health status of the API
    """
    return HealthCheckResponse.default()


@router.get("/ready", summary="Readiness Check")
async def readiness_check() -> JSONResponse:
    """
    Readiness check for Kubernetes/container orchestration.
    
    Returns:
        JSONResponse: Ready status
    """
    return JSONResponse(
        content={
            "status": "ready",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
        }
    )


@router.get("/live", summary="Liveness Check")
async def liveness_check() -> JSONResponse:
    """
    Liveness check for Kubernetes/container orchestration.
    
    Returns:
        JSONResponse: Alive status
    """
    return JSONResponse(
        content={
            "status": "alive",
            "timestamp": "2024-01-01T00:00:00Z",
        }
    )
