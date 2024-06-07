from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from main_router import router as main_router
from admin_router import router as admin_router

app = FastAPI(openapi_url="/ivr-unt/openapi.json")

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost",
    "https://ivr-urfu.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(main_router)
app.include_router(admin_router)
