from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from main_router import router as main_router
from admin_router import router as admin_router


app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://127.0.0.1:8000",
#     "http://localhost:8000",
#     "localhost:8000"
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(main_router)
app.include_router(admin_router)
