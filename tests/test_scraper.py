from src.sourcesync.scraper.engine import PlaywrightScraper

def test_scraper_initialization():
    scraper = PlaywrightScraper()
    assert scraper.headless == True
    assert scraper.page is None
    assert scraper.browser is None

def test_build_search_query():
    scraper = PlaywrightScraper()
    keywords = {
        'Skills': ['MuleSoft', 'OpenShift'],
        'Location': 'Remote',
        'Experience': '10'
    }
    query = scraper._build_search_query(keywords)
    assert 'MuleSoft' in query
    assert 'OpenShift' in query
    assert 'remote work' in query
    assert '10 years experience' in query
    assert 'site:linkedin.com/in' in query


def test_has_search_terms_returns_false_when_all_undetermined():
    scraper = PlaywrightScraper()
    keywords = {
        'Skills': [],
        'Location': 'Undetermined',
        'Experience': 'N/A'
    }

    assert scraper._has_search_terms(keywords) is False
