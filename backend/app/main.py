"""
FastAPI application entry point.

This is the main application file that configures and runs the FastAPI app.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import uvicorn

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.database.session import async_engine, create_tables
from app.api.v1.endpoints import (
    health,
    auth,
    users,
    products,
    categories,
    orders,
    cart,
    reviews,
)
from app.schemas.base import ErrorResponse


# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
    handlers=[
        logging.FileHandler(settings.LOG_FILE),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


# Lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.
    
    Handles startup and shutdown events.
    """
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Database URL: {settings.DATABASE_URL}")
    
    # Create tables if in development
    if settings.DEBUG:
        logger.info("Creating database tables...")
        await create_tables()
        logger.info("Database tables created")
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME}")
    await async_engine.dispose()


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    debug=settings.DEBUG,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    
    # OpenAPI configuration
    openapi_tags=[
        {
            "name": "Health",
            "description": "Health check endpoints",
        },
        {
            "name": "Authentication",
            "description": "User authentication and authorization",
        },
        {
            "name": "Users",
            "description": "User management",
        },
        {
            "name": "Products",
            "description": "Product management",
        },
        {
            "name": "Categories",
            "description": "Product category management",
        },
        {
            "name": "Orders",
            "description": "Order management",
        },
        {
            "name": "Cart",
            "description": "Shopping cart operations",
        },
        {
            "name": "Reviews",
            "description": "Product review management",
        },
    ],
)


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """Handle validation errors."""
    logger.warning(f"Validation error: {exc.errors()}")
    
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"],
        })
    
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            success=False,
            error="validation_error",
            message="Validation failed",
            details={"errors": errors},
        ).model_dump(),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
) -> JSONResponse:
    """Handle HTTP exceptions."""
    logger.error(f"HTTP error: {exc.status_code} - {exc.detail}")
    
    if isinstance(exc.detail, dict):
        detail = exc.detail
    else:
        detail = {"message": exc.detail}
    
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            error="http_error",
            message=detail.get("message", "An error occurred"),
            details=detail,
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            success=False,
            error="server_error",
            message="An unexpected error occurred",
        ).model_dump(),
    )


# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
    allow_credentials=True,
    expose_headers=["*"] if "*" in settings.CORS_HEADERS else settings.CORS_HEADERS,
    max_age=600,
)


# Mount static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)
app.mount(
    "/uploads",
    StaticFiles(directory=settings.UPLOAD_DIR),
    name="uploads",
)


# Include API routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
app.include_router(cart.router, prefix="/api/v1")
app.include_router(reviews.router, prefix="/api/v1")


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "docs": "/docs",
        "health": "/api/v1/health",
    }


# Run server (for development)
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=settings.DEBUG,
    )
