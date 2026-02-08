from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, responses, status
from fastapi.responses import JSONResponse
import time
from app.core.database import create_db_and_tables
from app.api import patients, users
import json

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create the database and tables if not present
    create_db_and_tables()
    yield
    # Shutdown (if needed in the future)
    pass

app = FastAPI(lifespan=lifespan)

# include_routes
app.include_router(patients.router)
app.include_router(users.router)

@app.get("/health")
def check_health():
    return {"message": "server is running"}

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exception: HTTPException):
    return JSONResponse(
        status_code = exception.status_code,
        content = {
            "success" : False,
            "error" : exception.detail,
            "method": request.method,
            "end_point": request.url.path,
        }
    )

@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    end = time.perf_counter()
    process_time = end-start
    response.headers["X-Process-Time"]= str(process_time * 1000) # in milliseconds
    return response

@app.middleware("http")
async def success_response_handler(request: Request, call_next):
    response = await call_next(request)
    
    # Skip OpenAPI/Swagger endpoints - they need to return schema as-is
    if request.url.path in ["/openapi.json", "/docs", "/redoc", "/openapi.yaml"]:
        return response
    
    # Only wrap successful JSON responses (status < 400)
    if response.status_code >= 400:
        return response
    
    # Check if response is JSON (skip file downloads, streaming, etc.)
    content_type = response.headers.get("content-type", "")
    if "application/json" not in content_type:
        return response
    
    # Read the response body from the iterator
    body_bytes = b""
    async for chunk in response.body_iterator:
        body_bytes += chunk
    
    # Parse the body
    try:
        body = json.loads(body_bytes.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # If parsing fails, return original body as string
        body = body_bytes.decode("utf-8", errors="ignore")
    
    # Wrap in success response format
    new_body = {
        "success": True,
        "data": body,
        "method": request.method,
        "end_point": request.url.path,
    }
    
    # Create new response preserving headers
    new_response = responses.JSONResponse(
        status_code=response.status_code, 
        content=new_body
    )
    # Copy headers from original response (except content-length which will be recalculated)
    for key, value in response.headers.items():
        if key.lower() != "content-length":
            new_response.headers[key] = value
    return new_response
    
@app.exception_handler(ValueError)
async def custom_value_error_handler(request: Request, exception: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "error": exception.args[0],
            "method": request.method,
            "end_point": request.url.path,
        }
    )

@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exception: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": exception.args[0],
            "method": request.method,
            "end_point": request.url.path,
        }
    )