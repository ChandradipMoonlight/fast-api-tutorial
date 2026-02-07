from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import time

from app.api import patients, users

app = FastAPI()

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