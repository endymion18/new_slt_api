from typing import Optional

from pydantic import BaseModel, HttpUrl


class Description(BaseModel):
    topic: str
    question: str
    description: str
    description_video: list[dict] = None


class DescriptionSl(BaseModel):
    topic: str
    question_sl: str = None
    description_sl: str = None
    description_video_sl: list[dict] = None


class SignLanguageSections(BaseModel):
    topic: str
    topic_video: Optional[HttpUrl] = None
    sections1_type: Optional[str] = None
    sections1: list[str]
    sections1_videos: Optional[list[HttpUrl]] = None
    sections1_additional: Optional[list[str]] = None
    sections1_additional_videos: Optional[list[HttpUrl]] = None
    sections2_type: Optional[str] = None
    sections2: Optional[list[str]] = None
    sections2_videos: Optional[list[HttpUrl]] = None
    sections2_additional: Optional[list[str]] = None
    sections2_additional_videos: Optional[list[HttpUrl]] = None


class SimpleLanguageSections(BaseModel):
    topic: str
    topic_icon: Optional[HttpUrl] = None
    sections1_type: Optional[str] = None
    sections1: list[str]
    sections1_icons: Optional[list[HttpUrl]] = None
    sections1_additional: Optional[list[str]] = None
    sections1_additional_icons: Optional[list[HttpUrl]] = None
    sections2_type: Optional[str] = None
    sections2: Optional[list[str]] = None
    sections2_icons: Optional[list[HttpUrl]] = None
    sections2_additional: Optional[list[str]] = None
    sections2_additional_icons: Optional[list[HttpUrl]] = None


class FullTextResult(BaseModel):
    rsl: Description
    sl: DescriptionSl
