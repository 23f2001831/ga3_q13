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
BASE_URL = "https://sanand0.github.io/tdsdata/js_table/?seed={seed}"

# Validate URL is set
if "example.com" in BASE_URL:
    print("ERROR: BASE_URL is still set to placeholder!")
    print("Update scrape_tables.py with actual URL before running.")
    sys.exit(1)

async def scrape_table_numbers(page, url: str, seed: int) -> list:
    """
    Scrape all numbers from tables on the page using JavaScript evaluation
    Returns list of numeric values found
    """
    try:
        print(f"  → Navigating to seed {seed}...")
        await page.goto(url, wait_until="networkidle", timeout=30000)
        
        # Wait for table to load
        print(f"  → Waiting for table element...")
        try:
            await page.wait_for_selector("table", timeout=10000)
        except:
            print(f"  ⚠ No table found, continuing anyway...")
        
        # Small wait to ensure JS is executed
        await page.wait_for_timeout(2000)
        
        # Use JavaScript to extract and sum all numbers from tables
        print(f"  → Extracting numbers from tables...")
        total_on_page = await page.evaluate(r'''() => {
            let total = 0;
            const numbers = [];
            const tables = document.querySelectorAll('table');
            for (const table of tables) {
                const cells = table.querySelectorAll('td, th');
                for (const cell of cells) {
                    const text = cell.innerText.trim();
                    if (text) {
                        const val = parseFloat(text);
                        if (!isNaN(val) && /^-?[0-9]+(?:\.[0-9]+)?$/.test(text)) {
                            total += val;
                            numbers.push(val);
                        }
                    }
                }
            }
            return {total: total, count: numbers.length};
        }''')
        
        count = total_on_page['count']
        total = total_on_page['total']
        print(f"  ✓ Found {count} numbers, sum on this page: {total}")
        
        # Return as list for compatibility
        return [total] if total != 0 else []
        
    except Exception as e:
        print(f"  ✗ ERROR scraping seed {seed}: {type(e).__name__}: {e}")
        return []

async def scrape_all_seeds():
    """
    Scrape all seeds and return total sum
    """
    page_totals = []
    
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
            page_totals.extend(numbers)
        
        await browser.close()
    
    # Calculate total
    total = sum(page_totals)
    return total, page_totals

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
