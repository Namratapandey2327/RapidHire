#!/usr/bin/env python3
"""
Test script to verify SourceSync X-ray search setup.
Run this to make sure everything is working before using the full application.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_browser():
    """Test that the browser can launch."""
    print("🔍 Testing browser launch...")
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.firefox.launch(headless=True)
            page = browser.new_page()
            page.goto("https://www.google.com")
            title = page.title()
            browser.close()

        print("✅ Browser works! Page title:", title)
        return True
    except Exception as e:
        print("❌ Browser test failed:", str(e))
        print("💡 Try: sudo apt-get install firefox")
        return False

def test_parser():
    """Test that the parser works."""
    print("🔍 Testing parser...")
    try:
        from sourcesync.analyzer.parser import analyze_candidate

        test_text = "Software Engineer Remote MuleSoft OpenShift 10+ years"
        result = analyze_candidate(test_text)

        print("✅ Parser works!")
        print(f"   Skills: {result['Skills']}")
        print(f"   Location: {result['Location']}")
        print(f"   Experience: {result['Experience']}")
        return True
    except Exception as e:
        print("❌ Parser test failed:", str(e))
        return False

def test_search():
    """Test a simple search."""
    print("🔍 Testing X-ray search...")
    try:
        from sourcesync.scraper.engine import PlaywrightScraper

        scraper = PlaywrightScraper()
        scraper.launch()

        # Simple test search
        keywords = {'Skills': ['Python'], 'Location': 'Remote', 'Experience': '5'}
        results = scraper.xray_search(keywords)
        scraper.close()

        print(f"✅ Search works! Found {len(results)} candidates")
        return True
    except Exception as e:
        print("❌ Search test failed:", str(e))
        return False

def main():
    print("🚀 SourceSync Setup Test")
    print("=" * 40)

    tests = [
        ("Browser Setup", test_browser),
        ("Parser Functionality", test_parser),
        ("X-ray Search", test_search)
    ]

    passed = 0
    for name, test_func in tests:
        print(f"\n📋 {name}:")
        if test_func():
            passed += 1
        print()

    print("=" * 40)
    print(f"Results: {passed}/{len(tests)} tests passed")

    if passed == len(tests):
        print("🎉 All tests passed! SourceSync is ready to use.")
        print("\nTry these commands:")
        print("  uvicorn backend.app:app --reload")
        print("  cd frontend && npm run dev")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")

if __name__ == "__main__":
    main()