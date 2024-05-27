import asyncio
import json
import os
import smtplib
import aiohttp
from email.message import EmailMessage
from pathlib import Path

from fastapi import FastAPI
from starlette.responses import FileResponse

from utils import get_sections

with open("../configs/api_config.json", "r") as f:
    config = json.load(f)
    es_url = config["base_url"]

requests_client: aiohttp.ClientSession | None = None
app = FastAPI()


@app.on_event("startup")
async def startup():
    global requests_client
    requests_client = aiohttp.ClientSession(es_url)


@app.on_event("shutdown")
async def shutdown():
    await requests_client.close()


@app.get("/ping")
async def ping():
    return "pong"


@app.get("/media/{path}")
async def get_avatar(path: str):
    os.chdir(".")
    img_path = Path(f"media/{path}")
    return FileResponse(img_path)


@app.get("/help")
async def send_email():
    msg = EmailMessage()
    msg['Subject'] = 'Необходима помощь'
    msg['From'] = config["sender"]
    msg['To'] = config["receiver"]

    msg.set_content("Подойдите, пожалуйста, к информационному стенду")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(config["sender"], config["sender_password"])
        server.send_message(msg)

    return {"success": "Email has been sent"}


@app.get("/get-description")
async def get_description(info: str):
    body = {
        "query": {
            "combined_fields": {
                "query": info,
                "fields": ["topic", "question"],
                "operator": "or"
            }
        }
    }
    async with requests_client.get(f"/mfc/_search", json=body) as response:
        if not response.ok:
            return {"error": "ElasticSearch error"}
        description = await response.json()
    return description["hits"]["hits"][0]


@app.get("/get-rsl-sections")
async def get_rsl_sections():
    async with requests_client.get(f"/rsl_sections/_search") as response:
        if not response.ok:
            return {"error": "ElasticSearch error"}
        return await get_sections(await response.json())


@app.get("/get-sl-sections")
async def get_sl_sections():
    async with requests_client.get(f"/sl_sections/_search") as response:
        if not response.ok:
            return {"error": "ElasticSearch error"}
        return await get_sections(await response.json())
