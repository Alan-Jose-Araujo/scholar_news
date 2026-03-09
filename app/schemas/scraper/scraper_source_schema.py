# scraper_source_schema.py
# @description Simple abstraction for the scraper source.
# @author Alan José <alanjsdelima@gmail.com>

from pydantic import BaseModel, Field, HttpUrl

class ScraperSourceSchema(BaseModel):

    name: str = Field(...)

    url: HttpUrl = Field(...)