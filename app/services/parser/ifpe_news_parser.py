# ifpe_news_parser.py
# @description News parser implementation for IFPE source.
# @author Alan José <alanjsdelima@gmail.com>

from app.services.parser.base_news_parser import BaseNewsParser
from bs4 import BeautifulSoup
from typing import Optional, List
from app.schemas.news.news_related_link_schema import NewsRelatedLink
from datetime import date

class IFPENewsParser(BaseNewsParser):

    def _parse_portuguese_date_string_(self, date_string: str) -> Optional[date]:
        import dateparser
        parsed_datetime = dateparser.parse(date_string, languages=["pt"])
        if not parsed_datetime:
            return None
        return parsed_datetime.date()

    def _extract_title_(self, soup: BeautifulSoup) -> str:
        title_soup = soup.find("h2", class_="noticia__titulo")
        if not title_soup:
            raise Exception("[Parse Exception] Error on extract title: Title element is None")
        return title_soup.get_text(strip=True)

    def _extract_summary_(self, soup: BeautifulSoup) -> Optional[str]:
        summary_soup = soup.find("div", class_="post__excerpt")
        if not summary_soup:
            return None
        return summary_soup.get_text(strip=True)

    def _extract_content_(self, soup: BeautifulSoup) -> str:
        content_soup = soup.find("div", class_="post__content")
        if not content_soup:
            raise Exception("[Parse Exception] Error on extract content: Content is None")
        content_thumbnail = content_soup.find("div", class_="post__thumb")
        # Remove thumbnail from content if present
        if content_thumbnail:
            content_thumbnail.decompose()
        return content_soup.get_text(strip=True)

    def _extract_thumbnail_url_(self, soup: BeautifulSoup) -> Optional[str]:
        thumbnail_imgs = soup.select("div.post__thumb img")
        if not thumbnail_imgs:
            return None
        img = thumbnail_imgs[0]
        return img.get("src") or img.get("srcset") or img.get("data-src")

    def _extract_publish_date_(self, soup: BeautifulSoup) -> Optional[date]:
        publish_date_soup = soup.find("span", class_="post__published")
        if not publish_date_soup:
            return None
        publish_date_text = publish_date_soup.get_text(strip=True).removeprefix("publicado em ")
        return self._parse_portuguese_date_string_(publish_date_text)

    def _extract_last_update_date_(self, soup: BeautifulSoup) -> Optional[date]:
        last_updated_date = soup.find("span", class_="post__updated")
        if not last_updated_date:
            return None
        updated_date_text = last_updated_date.get_text(strip=True).removeprefix("última modificação em ")
        return self._parse_portuguese_date_string_(updated_date_text)

    def _extract_related_links_(self, soup: BeautifulSoup) -> List[NewsRelatedLink]:
        anchors = soup.select("a")
        related_links: List[NewsRelatedLink] = []
        for anchor in anchors:
            link_href = anchor.get("href")
            if not link_href:
                continue  # skip anchors without href
            link_text = anchor.get_text(strip=True)
            try:
                related_link = NewsRelatedLink(text=link_text, url=link_href)
                related_links.append(related_link)
            except Exception as e:
                # Optionally log or print the error
                continue
        return related_links


    def page_has_next_pagination_link(self, html_text: str) -> bool:
        soup = BeautifulSoup(html_text, "html.parser")
        if not soup:
            return False
        pagination_links = soup.select("li.page-item a.page-link")
        if not pagination_links:
            return False
        last_link_text = pagination_links[-1].get_text(strip=True).lower()
        return "próxima" in last_link_text or "próximo" in last_link_text

    def get_article_links_from_index_page(self, html_text: str) -> List[str]:
        soup = BeautifulSoup(html_text, "html.parser")
        if not soup:
            return []
        articles = soup.find_all("article", class_="noticia")
        article_links: List[str] = []
        for article in articles:
            article_anchor = article.find("a", class_="noticia__link")
            if article_anchor:
                href = article_anchor.get("href")
                if href:
                    article_links.append(href)
        return article_links