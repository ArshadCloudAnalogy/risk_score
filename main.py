from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from routers import api_router
import time
import logging
from mangum import Mangum

app = FastAPI(title="RiskCore API", version="1.0.0",
              docs_url="/api/v1/swagger/_docs")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://risk-score-fe.vercel.app",
                   "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = f"{request.method} {request.url.path}"
    logging.info(f"⬅️ Start request: {idem}")
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time
    logging.info(f"➡️ Completed in {duration:.2f}s: {idem}")
    response.headers["X-Process-Time"] = str(duration)
    return response


@app.get("/api/v1/")
def root():
    return {"message": "Welcome to RiskCore API"}


# Routers
app.include_router(api_router)

handler = Mangum(app)
