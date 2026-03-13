# base_news_parser.py
# @description An abstract news parser to implements common news parsing.
# @author Alan José <alanjsdelima@gmail.com>

from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from typing import Optional, List
from app.schemas.news.news_related_link_schema import NewsRelatedLink
from app.schemas.news.news_schema import NewsSchema
from datetime import date
from pydantic import ValidationError

class BaseNewsParser(ABC):

    @abstractmethod
    def _extract_title_(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def _extract_summary_(self, soup: BeautifulSoup) -> Optional[str]:
        pass

    @abstractmethod
    def _extract_content_(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def _extract_thumbnail_url_(self, soup: BeautifulSoup) -> Optional[str]:
        pass

    @abstractmethod
    def _extract_publish_date_(self, soup: BeautifulSoup) -> Optional[date]:
        pass

    @abstractmethod
    def _extract_last_update_date_(self, soup: BeautifulSoup) -> Optional[date]:
        pass

    @abstractmethod
    def _extract_related_links_(self, soup: BeautifulSoup) -> List[NewsRelatedLink]:
        pass

    @abstractmethod
    def page_has_next_pagination_link(self, html_text: str) -> bool:
        pass

    @abstractmethod
    def get_article_links_from_index_page(self, html_text: str) -> List[str]:
        pass

    def parse(self, html_text: str) -> NewsSchema:
        try:
            soup: BeautifulSoup = BeautifulSoup(html_text, "html.parser")
            if not soup:
                raise ValueError("[Parse Exception] Error on parse news: soup is None.")
            related_links: List[NewsRelatedLink] = self._extract_related_links_(soup)
            thumbnail_url: Optional[str] = self._extract_thumbnail_url_(soup)
            news_data: dict = {
                "title": self._extract_title_(soup),
                "summary": self._extract_summary_(soup),
                "content": self._extract_content_(soup),
                "thumbnail_url": thumbnail_url,
                "publish_date": self._extract_publish_date_(soup),
                "last_update_date": self._extract_last_update_date_(soup),
                "related_links": related_links
            }
            news = NewsSchema(**news_data)
            return news
        except ValidationError as error:
            print(f"[ValidationError] {error}")
            raise
        except Exception as exception:
            print(f"[Parse Exception] {exception}")
            raise