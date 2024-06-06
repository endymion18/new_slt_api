from fastapi import FastAPI
from main_router import router as main_router
from admin_router import router as admin_router

app = FastAPI()


app.include_router(main_router)
app.include_router(admin_router)
