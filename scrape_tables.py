"""
Automated QA with Playwright and GitHub Actions
Scrapes all numbers from dynamically generated tables (seeds 71-80) and computes the sum
"""

import asyncio
import re
import sys
from playwright.async_api import async_playwright

# Seeds to scrape
SEEDS = list(range(71, 81))  # 71 to 80

# ⚠️ IMPORTANT: Update this with the actual base URL for your seeds
# Example: "https://example.com/generate?seed={seed}"
BASE_URL = "https://example.com/seed/{seed}"

# Validate URL is set
if "example.com" in BASE_URL:
    print("ERROR: BASE_URL is still set to placeholder!")
    print("Update scrape_tables.py with actual URL before running.")
    sys.exit(1)

async def scrape_table_numbers(page, url: str, seed: int) -> list:
    """
    Scrape all numbers from tables on the page
    Returns list of numeric values found
    """
    try:
        print(f"  → Navigating to seed {seed}...")
        await page.goto(url, wait_until="networkidle", timeout=30000)
        
        # Wait for table to load
        print(f"  → Waiting for table element...")
        await page.wait_for_selector("table", timeout=10000)
        
        # Extract all text from tables
        print(f"  → Extracting table content...")
        table_content = await page.locator("table").all_text_contents()
        
        # Find all numbers (integers and decimals)
        numbers = []
        for content in table_content:
            # Match integers and decimals
            matches = re.findall(r'-?\d+(?:\.\d+)?', content)
            for match in matches:
                try:
                    if '.' in match:
                        numbers.append(float(match))
                    else:
                        numbers.append(int(match))
                except ValueError:
                    pass
        
        print(f"  ✓ Found {len(numbers)} numbers on seed {seed}")
        return numbers
    except Exception as e:
        print(f"  ✗ ERROR scraping seed {seed}: {type(e).__name__}: {e}")
        return []

async def scrape_all_seeds():
    """
    Scrape all seeds and return total sum
    """
    all_numbers = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Set a longer default timeout
        page.set_default_timeout(30000)
        page.set_default_navigation_timeout(30000)
        
        for seed in SEEDS:
            url = BASE_URL.format(seed=seed)
            print(f"\nScraping seed {seed}:")
            
            numbers = await scrape_table_numbers(page, url, seed)
            all_numbers.extend(numbers)
        
        await browser.close()
    
    # Calculate total
    total = sum(all_numbers)
    return total, all_numbers

async def main():
    """Main entry point"""
    print("="*70)
    print("DataDash QA Automation - Table Sum Calculator")
    print("="*70)
    print(f"Base URL: {BASE_URL}")
    print(f"Seeds: {min(SEEDS)} to {max(SEEDS)}")
    print("="*70 + "\n")
    
    try:
        total, all_numbers = await scrape_all_seeds()
        
        print("\n" + "="*70)
        print(f"TOTAL NUMBERS FOUND: {len(all_numbers)}")
        print(f"TOTAL SUM: {total}")
        print("="*70 + "\n")
        
        # Print in a format easy to parse from logs
        print(f"RESULT: SUM={total}")
        
    except Exception as e:
        print(f"\nFATAL ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    print(f"\nScraping seeds: {min(SEEDS)} to {max(SEEDS)}")
    print(f"Base URL: {BASE_URL}\n")
    
    total, all_numbers = await scrape_all_seeds()
    
    print(f"\n{'='*60}")
    print(f"TOTAL NUMBERS FOUND: {len(all_numbers)}")
    print(f"TOTAL SUM: {total}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    asyncio.run(main())
