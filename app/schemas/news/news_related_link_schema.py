# new_related_link_schema.py
# @description A link abstraction with text, url and schema.
# @author Alan José <alanjsdelima@gmail.com>

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from app.schemas.news.http_link_schema_enum import HttpLinkSchemaEnum

class NewsRelatedLink(BaseModel):

    text: Optional[str] = Field(default=None)

    url: HttpUrl = Field(...)

    http_schema: HttpLinkSchemaEnum = Field(..., default=HttpLinkSchemaEnum.HTTPS)