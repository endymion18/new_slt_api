import os
import smtplib
from aiohttp import ClientSession, ClientConnectorError
import json
from email.message import EmailMessage
from pathlib import Path
from fastapi import APIRouter
from starlette.responses import FileResponse

from models import Description, SignLanguageSections, SimpleLanguageSections, DescriptionSl, FullTextResult
from utils import get_sections

with open("./configs/api_config.json", "r") as f:
    config = json.load(f)
    es_url = config["base_url"]

router = APIRouter()
requests_client: ClientSession | None = None


@router.on_event("startup")
async def startup():
    global requests_client
    requests_client = ClientSession(es_url, trust_env=True)


@router.on_event("shutdown")
async def shutdown():
    await requests_client.close()


@router.get("/ping",
            description="Check if interface is available",
            response_description="Returns \"pong\" if ok")
async def ping():
    return "pong"


@router.get("/media/{path}",
            description="Get file (image/video) from server by name",
            response_description="Returns file")
async def get_avatar(path: str):
    os.chdir(".")
    img_path = Path(f"media/{path}")
    return FileResponse(img_path)


@router.post("/help",
             description="Send message to email specified in configs/api_config.json"
             )
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


@router.get("/get-description",
            description="Get description of section by string of section name and subsection name",
            response_model=Description | dict)
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
        description = description["hits"]["hits"]
    if len(description) != 0:
        return description[0]["_source"]
    return {"error": "Nothing found by your request"}


@router.get("/get-description-sl",
            description="Get description of section for simple language by string of section name and subsection name",
            response_model=DescriptionSl | dict)
async def get_sl_description(info: str):
    body = {
        "query": {
            "combined_fields": {
                "query": info,
                "fields": ["topic", "question", "question_sl"],
                "operator": "or"
            }
        }
    }
    async with requests_client.get(f"/mfc/_search", json=body) as response:
        if not response.ok:
            return {"error": "ElasticSearch error"}
        description = await response.json()
        description = description["hits"]["hits"]
    if len(description) != 0:
        if "question_sl" in description[0]["_source"]:
            return DescriptionSl(**description[0]["_source"])
        else:
            return DescriptionSl(topic=description[0]["_source"]["topic"],
                                 question_sl=description[0]["_source"]["question"],
                                 description_sl=description[0]["_source"]["description"])
    return {"error": "Nothing found by your request"}


@router.get("/search",
            description="Full-text search in knowledge base",
            response_model=FullTextResult | dict)
async def fulltext_search(info: str):
    body = {
        "query": {
            "combined_fields": {
                "query": info,
                "fields": ["topic", "question", "description"],
                "operator": "or"
            }
        }
    }
    async with requests_client.get(f"/mfc/_search", json=body) as response:
        if not response.ok:
            return {"error": "ElasticSearch error"}
        description = await response.json()
    if len(description["hits"]["hits"]) != 0:
        description = description["hits"]["hits"][0]["_source"]
        if "question_sl" in description:
            sl = DescriptionSl(**description)
        else:
            sl = DescriptionSl(topic=description["topic"],
                               question_sl=description["question"],
                               description_sl=description["description"])
        rsl = Description(**description)

        return FullTextResult(rsl=rsl, sl=sl)
    return {"error": "Nothing found by your request"}


@router.get("/get-rsl-sections",
            description="Get sections for sign language",
            response_model=list[SignLanguageSections] | dict)
async def get_rsl_sections():
    try:
        async with requests_client.get(f"/rsl_sections/_search") as response:
            if not response.ok:
                return {"error": "ElasticSearch error"}
            return await get_sections(await response.json())
    except ClientConnectorError:
        return {"error": "Can't connect to ElasticSearch"}


@router.get("/get-sl-sections",
            description="Get sections for simple language",
            response_model=list[SimpleLanguageSections] | dict)
async def get_sl_sections():
    try:
        async with requests_client.get(f"/sl_sections/_search") as response:
            if not response.ok:
                return {"error": "ElasticSearch error"}
            return await get_sections(await response.json())
    except ClientConnectorError:
        return {"error": "Can't connect to ElasticSearch"}
