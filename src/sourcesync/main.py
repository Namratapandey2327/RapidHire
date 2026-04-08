import argparse
from .analyzer.parser import analyze_candidate
from .scraper.engine import PlaywrightScraper


def run_analysis(text: str):
    """Run candidate analysis and return the parsed results."""
    return analyze_candidate(text)


def run_xray_search(keywords: dict):
    """Run X-ray search using DuckDuckGo with parsed keywords."""
    scraper = PlaywrightScraper(headless=True)

    if not (keywords.get('Skills') or (keywords.get('Location') and keywords['Location'] != 'Undetermined') or (keywords.get('Experience') and keywords['Experience'] != 'N/A')):
        print("No usable search keywords found. Please include skills, location, or experience in the job description.")
        return []

    try:
        scraper.launch()
        results = scraper.xray_search(keywords)
        return results
    except Exception as e:
        print(f"X-ray search failed: {e}")
        return []
    finally:
        try:
            scraper.close()
        except:
            pass


def main():
    parser = argparse.ArgumentParser(description="SourceSync candidate analyzer and X-ray search")
    parser.add_argument("--analyze", help="Analyze candidate profile text")
    parser.add_argument("--search", help="Perform X-ray search using parsed keywords from job description")

    args = parser.parse_args()

    if args.analyze:
        results = run_analysis(args.analyze)
        print("Visa:", results["Visa"])
        print("Location:", results["Location"])
        print("Experience:", results["Experience"], "Years")
        print("Skills:", ", ".join(results["Skills"]) if results["Skills"] else "None detected")

    elif args.search:
        # Parse the job description first
        parsed_keywords = run_analysis(args.search)
        print("Parsed keywords from JD:")
        print("Skills:", parsed_keywords["Skills"])
        print("Location:", parsed_keywords["Location"])
        print("Experience:", parsed_keywords["Experience"])
        print()

        # Perform X-ray search
        print("Performing X-ray search on DuckDuckGo...")
        search_results = run_xray_search(parsed_keywords)

        print(f"\nFound {len(search_results)} potential candidates:")
        for i, candidate in enumerate(search_results, 1):
            print(f"{i}. {candidate['name']}")
            print(f"   Headline: {candidate['headline']}")
            if candidate['profile_url']:
                print(f"   Profile: {candidate['profile_url']}")
            print()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
