import json
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from fastapi import FastAPI
from starlette.responses import FileResponse

app = FastAPI()

with open("../configs/email.json", "r") as f:
    email_config = json.load(f)


@app.get("/ping")
async def ping():
    return "pong"


@app.get("/media/{path}")
async def get_avatar(path: str):
    os.chdir(".")
    img_path = Path(f"media/{path}")
    print(img_path)
    return FileResponse(img_path)


@app.get("/help")
async def send_email():
    msg = EmailMessage()
    msg['Subject'] = 'Необходима помощь'
    msg['From'] = email_config["sender"]
    msg['To'] = email_config["receiver"]

    msg.set_content("Подойдите, пожалуйста, к информационному стенду")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(email_config["sender"], email_config["sender_password"])
        server.send_message(msg)

    return {"success": "Email has been sent"}


@app.get("/search")
async def search(info: str):
    return None


@app.get("/get-all-sections")
async def get_all_sections():
    return None
