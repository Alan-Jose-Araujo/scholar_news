import os
import pytest
from app.services.parser.ifpe_news_parser import IFPENewsParser

@pytest.fixture
def index_html():
    path = os.path.join(os.path.dirname(__file__), '../../static_files/ifpe_news_index_dummy_page.html')
    with open(path, encoding='utf-8') as f:
        return f.read()

def test_get_article_links_from_index_page(index_html):
    parser = IFPENewsParser()
    links = parser.get_article_links_from_index_page(index_html)
    # There are 12 articles in the provided HTML
    assert isinstance(links, list)
    assert len(links) == 16
    # Check that the first link is correct
    assert links[0] == "https://portal.ifpe.edu.br/noticias/jovens-de-escolas-publicas-de-pernambuco-podem-se-candidatar-a-formacao-em-enfermagem-na-alemanha/"
    # Check that all links are unique
    assert len(set(links)) == len(links)

def test_page_has_next_pagination_link(index_html):
    parser = IFPENewsParser()
    assert parser.page_has_next_pagination_link(index_html) is True
    # Remove 'Próxima Página' to test False
    html_no_next = index_html.replace('Próxima Página', '')
    assert parser.page_has_next_pagination_link(html_no_next) is False
