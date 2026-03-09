# new_schema.py
# @description A news object abstraction to handle database and holds the retrieved news data.
# @author Alan José <alanjsdelima@gmail.com>

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import date, datetime
from app.schemas.news.news_related_link_schema import HttpLinkSchemaEnum

class NewsSchema(BaseModel):

    id: Optional[int] = Field(default=None)

    title: str = Field(..., min_length=1)

    summary: Optional[str] = Field(default=None)

    content: str = Field(..., min_length=1)

    thumbnail_url: Optional[HttpUrl] = Field(default=None)

    publish_date: Optional[date] = Field(default=None)

    last_update_date: Optional[date] = Field(default=None)

    related_links: List[HttpLinkSchemaEnum] = Field(default=[])

    scraped_on_page: Optional[int] = Field(default=None)

    scraped_at: datetime = Field(..., default_factory=datetime.now)