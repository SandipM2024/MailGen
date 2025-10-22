from fastapi import FastAPI
from app.core.config import settings
from app.database.base import Base
from app.database.session import engine
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
# from app.api.routes.account_router import router as account_router
from app.router.mailgen_router import router as mailgen_router


# from app.api.routes.demo_router import router as demo_router
app = FastAPI()

origins = ["*"]  # Allows all origins; change this to a specific domain for better security

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allowed origins
    allow_credentials=True,           # Allow cookies/auth headers
    allow_methods=["*"],              # Allowed HTTP methods
    allow_headers=["*"],              # Allowed HTTP headers
)


security = HTTPBearer()
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema    
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="1.0.0",        
        routes=app.routes,
    )  
    if "components" in openapi_schema:
        if "securitySchemes" in openapi_schema["components"]:
            openapi_schema["components"]["securitySchemes"]["HTTPBearer"] = {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Enter **only** the token. Do not add 'Bearer '."
            }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapi

# app.mount("/media", StaticFiles(directory="media"), name="media")

# Include routes
app.include_router(mailgen_router, prefix=f"{settings.API_V1_STR}/mailgen",tags=["MailGen API"])


@app.get("/")
def root():
    return {"message": "Mail Gen Api."}
