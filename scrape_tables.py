"""
Automated QA with Playwright and GitHub Actions
Scrapes all numbers from dynamically generated tables (seeds 71-80) and computes the sum
"""

import asyncio
import re
from playwright.async_api import async_playwright

# Seeds to scrape
SEEDS = list(range(71, 81))  # 71 to 80

# Base URL template
BASE_URL = "https://example.com/seed/{seed}"  # Replace with actual base URL
# For IITM, it's likely something like the q14 structure
# Adjust based on actual website structure

async def scrape_table_numbers(page, url: str) -> list:
    """
    Scrape all numbers from tables on the page
    Returns list of numeric values found
    """
    try:
        await page.goto(url, wait_until="networkidle")
        
        # Wait for table to load
        await page.wait_for_selector("table", timeout=5000)
        
        # Extract all text from tables
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
        
        return numbers
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

async def scrape_all_seeds():
    """
    Scrape all seeds and return total sum
    """
    all_numbers = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        for seed in SEEDS:
            url = BASE_URL.format(seed=seed)
            print(f"Scraping seed {seed}: {url}")
            
            numbers = await scrape_table_numbers(page, url)
            all_numbers.extend(numbers)
            
            print(f"  Found {len(numbers)} numbers on seed {seed}")
        
        await browser.close()
    
    # Calculate total
    total = sum(all_numbers)
    return total, all_numbers

async def main():
    """Main entry point"""
    print("="*60)
    print("DataDash QA Automation - Table Sum Calculator")
    print("="*60)
    print(f"\nScraping seeds: {min(SEEDS)} to {max(SEEDS)}")
    print(f"Base URL: {BASE_URL}\n")
    
    total, all_numbers = await scrape_all_seeds()
    
    print(f"\n{'='*60}")
    print(f"TOTAL NUMBERS FOUND: {len(all_numbers)}")
    print(f"TOTAL SUM: {total}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    asyncio.run(main())
