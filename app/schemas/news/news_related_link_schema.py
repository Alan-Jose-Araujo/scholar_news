# new_related_link_schema.py
# @description A link abstraction with text, url and schema.
# @author Alan José <alanjsdelima@gmail.com>

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional

class NewsRelatedLink(BaseModel):

    text: Optional[str] = Field(default=None)

    url: HttpUrl = Field(...)

    def has_insecure_schema(self) -> bool :
        return not "https" in str(self.url)