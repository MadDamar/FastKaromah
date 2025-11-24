from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from app.config import settings
from app.database import engine, Base

# Import semua routers
from app.routers.auth import router as auth_router
from app.routers.customer import router as customer_router
from app.routers.transaksi import router as transaksi_router
from app.routers.checkout import router as checkout_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    try:
        # Startup
        print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
        print(f"Environment: {'Development' if settings.DEBUG else 'Production'}")
        
        # Skip table creation since tables already exist from Laravel
        print("Skipping table creation (tables exist from Laravel)")
        
        yield
        
    except Exception as e:
        print(f"Startup error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        # Shutdown
        try:
            await engine.dispose()
            print("Database connections closed")
        except Exception as e:
            print(f"Shutdown error: {e}")


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="FastAPI Backend with JWT Authentication",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)


# Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with custom response"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error", "errors": errors},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    import traceback
    
    # Log full error in debug mode
    if settings.DEBUG:
        error_detail = {
            "error": str(exc),
            "type": type(exc).__name__,
            "traceback": traceback.format_exc()
        }
        print(f"\n❌ ERROR: {error_detail}\n")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_detail,
        )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


# Include routers
app.include_router(auth_router, prefix="/api/v1")
print("✅ Auth router registered")

app.include_router(customer_router, prefix="/api/v1")
print("✅ Customer router registered")

app.include_router(transaksi_router, prefix="/api/v1")
print("✅ Transaksi router registered")

app.include_router(checkout_router, prefix="/api/v1")
print("✅ Checkout router registered")
# Debug routes
if settings.DEBUG:
    print("\n📋 Registered API Routes:")
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            if '/api/v1' in route.path:
                print(f"  {list(route.methods)} {route.path}")
    print()


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs" if settings.DEBUG else "Disabled in production",
    }