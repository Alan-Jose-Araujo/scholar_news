import os
import pytest
from app.services.parser.ifpe_news_parser import IFPENewsParser

@pytest.fixture
def article_html():
    path = os.path.join(os.path.dirname(__file__), '../../static_files/ifpe_news_article_dummy_page.html')
    with open(path, encoding='utf-8') as f:
        return f.read()

def normalize(s):
        return ' '.join(s.split())

def test_extract_title(article_html):
    parser = IFPENewsParser()
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(article_html, 'html.parser')
    title = parser._extract_title_(soup)
    assert title == 'Aberta oportunidade para estudantes estudarem e trabalharem com enfermagem na Alemanha'

def test_extract_summary(article_html):
    parser = IFPENewsParser()
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(article_html, 'html.parser')
    summary = parser._extract_summary_(soup)
    expected_summary: str = 'Programa oferece curso de alemão com bolsa no Recife e formação profissional remunerada em instituições alemãs. Inscrições até 25/3'
    # Normalize whitespace for comparison
    assert normalize(summary) == normalize(expected_summary)

def test_extract_content(article_html):
    parser = IFPENewsParser()
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(article_html, 'html.parser')
    content = parser._extract_content_(soup)
    assert 'Estudantes e egressos do IFPE que concluíram o ensino médio têm uma nova oportunidade de formação internacional.' in normalize(content)
    assert 'Dúvidas podem ser esclarecidas com o Departamento de Relações Internacionais (DRIN) pelo e-mail: internacional@reitoria.ifpe.edu.br' in normalize(content)

def test_extract_thumbnail_url(article_html):
    parser = IFPENewsParser()
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(article_html, 'html.parser')
    thumbnail_url = parser._extract_thumbnail_url_(soup)
    assert thumbnail_url.endswith('padrao-site_bannersite-oportunidade-1-350x210.png')

def test_extract_publish_date(article_html):
    parser = IFPENewsParser()
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(article_html, 'html.parser')
    publish_date = parser._extract_publish_date_(soup)
    assert str(publish_date) == '2026-03-12'

def test_extract_last_update_date(article_html):
    parser = IFPENewsParser()
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(article_html, 'html.parser')
    last_update = parser._extract_last_update_date_(soup)
    assert str(last_update) == '2026-03-12'

def test_extract_related_links(article_html):
    parser = IFPENewsParser()
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(article_html, 'html.parser')
    content_soup: BeautifulSoup = soup.find("div", class_="post__content")
    related_links = parser._extract_related_links_(content_soup)
    # There should be several links, including the CCBA link
    assert any('ccba.org.br' in str(l.url) for l in related_links)
    assert any('acesse aqui o site do CCBA.' in l.text for l in related_links)

def test_parse_full_article(article_html):
    parser = IFPENewsParser()
    news = parser.parse(article_html)
    assert normalize(news.title) == 'Aberta oportunidade para estudantes estudarem e trabalharem com enfermagem na Alemanha'
    assert normalize(news.summary) == 'Programa oferece curso de alemão com bolsa no Recife e formação profissional remunerada em instituições alemãs. Inscrições até 25/3'
    assert 'Estudantes e egressos do IFPE' in normalize(news.content)
    assert str(news.thumbnail_url).endswith('padrao-site_bannersite-oportunidade-1-350x210.png')
    assert str(news.publish_date) == '2026-03-12'
    assert str(news.last_update_date) == '2026-03-12'
    assert any('ccba.org.br' in str(l.url) for l in news.related_links)
