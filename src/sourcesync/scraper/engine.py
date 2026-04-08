from playwright.sync_api import sync_playwright
from .selectors import *
import time
import urllib.parse

class PlaywrightScraper:
    """Browser automation helper for SourceSync X-ray search using DuckDuckGo."""

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.page = None
        self.browser = None
        self._playwright = None

    def launch(self):
        """Launch a Playwright browser session."""
        self._playwright = sync_playwright().start()
        self.browser = self._playwright.firefox.launch(headless=self.headless)
        self.page = self.browser.new_page()
        return self.page

    def _build_search_query(self, keywords: dict):
        """Build a search query from parsed keywords for X-ray search."""
        query_parts = []

        # Add job title first (most important)
        if keywords.get('Job Title') and keywords['Job Title'] != 'Undetermined':
            job_title = keywords['Job Title']
            query_parts.append(f'"{job_title}"')

        # Add skills
        if keywords.get('Skills'):
            skills_query = ' '.join(
                f'"{skill}"' if ' ' in skill else skill
                for skill in keywords['Skills'][:4]
            )
            query_parts.append(skills_query)

        # Add location
        if keywords.get('Location') and keywords['Location'] != 'Undetermined':
            location = keywords['Location']
            if location == 'Remote':
                query_parts.append('remote work remote position')
            elif location == 'Offshore':
                query_parts.append('offshore offshore development')
            else:
                query_parts.append(f'"{location}"')

        # Add experience
        if keywords.get('Experience') and keywords['Experience'] != 'N/A':
            years = keywords['Experience']
            query_parts.append(f'{years} years experience {years}+ years')

        # Add common candidate search terms
        query_parts.extend([
            'site:linkedin.com/in',
            '-site:linkedin.com/company',
            'software engineer developer engineer'
        ])

        return ' '.join(query_parts)

    def _has_search_terms(self, keywords: dict) -> bool:
        """Return True when parsed keywords contain enough searchable terms."""
        return bool(
            (keywords.get('Job Title') and keywords['Job Title'] != 'Undetermined') or
            keywords.get('Skills') or
            (keywords.get('Location') and keywords['Location'] != 'Undetermined') or
            (keywords.get('Experience') and keywords['Experience'] != 'N/A')
        )

    def xray_search(self, keywords: dict):
        """
        Perform X-ray search using DuckDuckGo with parsed keywords.

        Args:
            keywords: Dict with keys like 'Skills', 'Location', 'Experience'
        """
        if not self.page:
            raise Exception("Browser not launched. Call launch() first.")

        if not self._has_search_terms(keywords):
            print("Search skipped: no usable keywords found in the job description.")
            return []

        # Build search query
        search_query = self._build_search_query(keywords)
        print(f"Searching DuckDuckGo with query: {search_query}")

        try:
            # Navigate to DuckDuckGo
            self.page.goto("https://duckduckgo.com", wait_until="domcontentloaded")
            time.sleep(2)

            # Enter search query
            search_box = self.page.locator(SEARCH_INPUT).first
            search_box.fill(search_query)
            time.sleep(1)
            search_box.press("Enter")

            # Wait for results to load and render
            self.page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(3)

            # Extract search results
            results = []
            try:
                result_items = self.page.locator(RESULT_ITEM).all()[:12]  # Limit to first 12 results

                for item in result_items:
                    try:
                        title = item.inner_text().strip()
                        url = item.get_attribute('href') or ""

                        # Attempt to find a snippet from the result block
                        snippet_elem = item.locator("xpath=ancestor::div[contains(@class, 'result')]//div[contains(@class, 'result__snippet')]")
                        snippet = snippet_elem.first.inner_text().strip() if snippet_elem.count() > 0 else ""

                        # Only include LinkedIn profile links
                        if url and 'linkedin.com/in/' in url and 'linkedin.com/company' not in url:
                            candidate = {
                                'name': title.replace(' - LinkedIn', '').strip(),
                                'headline': snippet[:200] + '...' if len(snippet) > 200 else snippet,
                                'profile_url': url,
                                'source': 'DuckDuckGo Search'
                            }
                            results.append(candidate)
                    except Exception as e:
                        print(f"Error parsing result: {e}")
                        continue
            except Exception as e:
                print(f"Error extracting results: {e}")

            return results

        except Exception as e:
            print(f"Search failed: {e}")
            return []

    def close(self):
        """Close the browser session."""
        if hasattr(self, "browser") and self.browser:
            self.browser.close()
        if hasattr(self, "_playwright") and self._playwright:
            self._playwright.stop()
