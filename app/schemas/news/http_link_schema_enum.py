# http_link_schema_enum.py
# @description Link http backed enum.
# @author Alan José <alanjsdelima@gmail.com>

from enum import Enum

class HttpLinkSchemaEnum(str, Enum):

    HTTP: str = "http"

    HTTPS: str = "https"