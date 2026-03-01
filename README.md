# Q13: Automated QA with Playwright and GitHub Actions

## Overview
This solution automates QA for data tables using Playwright and GitHub Actions. It scrapes numbers from dynamically generated tables across multiple seed pages and computes their sum.

## Features
- ✅ Playwright async scraping of 10 seed pages (71-80)
- ✅ Extracts all numbers from HTML tables
- ✅ Computes total sum of all numbers
- ✅ Runs as GitHub Action on push/PR/schedule
- ✅ Student email in workflow step name
- ✅ Detailed logging in GitHub Actions

## Files

### scrape_tables.py
Main script that:
1. Visits seeds 71-80
2. Waits for tables to load with Playwright
3. Extracts all numeric values using regex
4. Sums all numbers
5. Prints results to console

**Update the BASE_URL** with the actual website URL:
```python
BASE_URL = "https://example.com/seed/{seed}"
```

### .github/workflows/qa-automation.yml
GitHub Actions workflow that:
- Runs on push, PR, and daily schedule
- Installs Python and Playwright
- Executes the scraping script
- Logs results
- **Includes student email in step name**: `23f2001831@ds.study.iitm.ac.in`

## Setup Instructions

### 1. Create GitHub Repository
```bash
git init
git add .
git commit -m "Add DataDash QA automation"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Enable GitHub Actions
- Go to your repository
- Click "Actions" tab
- Click "Enable GitHub Actions"

### 3. Run Locally (Optional)
```bash
cd ga3/q13
python -m pip install -r requirements.txt
playwright install chromium
python scrape_tables.py
```

## Sample Output

```
============================================================
DataDash QA Automation - Table Sum Calculator
============================================================

Scraping seeds: 71 to 80
Base URL: https://example.com/seed/{seed}

Scraping seed 71: https://example.com/seed/71
  Found 45 numbers on seed 71
Scraping seed 72: https://example.com/seed/72
  Found 48 numbers on seed 72
...

============================================================
TOTAL NUMBERS FOUND: 450
TOTAL SUM: 1234567
============================================================
```

## GitHub Actions Features

### Triggers
- **Push**: Runs on every commit to main
- **Pull Request**: Runs on every PR to main
- **Schedule**: Runs daily at 2 AM UTC (configurable)

### Email in Workflow
The workflow includes the student email in the step name:
```yaml
- name: Run QA - Student 23f2001831@ds.study.iitm.ac.in Table Validation
```

This ensures the email is visible in:
- GitHub Actions logs
- Workflow run history
- Email notifications

## Customization

### Change Base URL
Edit `scrape_tables.py`:
```python
BASE_URL = "https://your-actual-domain.com/seed/{seed}"
```

### Change Seeds
Edit `scrape_tables.py`:
```python
SEEDS = list(range(71, 81))  # Change range as needed
```

### Change Schedule
Edit `.github/workflows/qa-automation.yml`:
```yaml
schedule:
  - cron: '0 2 * * *'  # Change cron expression
```

Cron reference: https://crontab.guru/

## Viewing Results

1. Go to your GitHub repository
2. Click "Actions" tab
3. Click on the workflow run
4. Click "scrape-and-verify" job
5. Expand "Run QA - Student..." step to see output

The logs will show:
- Total numbers found
- Total sum
- Any errors during scraping

## Troubleshooting

### Playwright installation fails
```bash
playwright install --with-deps
```

### Timeout errors
Increase wait timeouts in `scrape_tables.py`:
```python
await page.wait_for_selector("table", timeout=10000)  # 10 seconds
```

### No numbers found
Check that the URL structure is correct and tables exist on those pages.

## Key Technologies
- **Playwright**: Async browser automation
- **GitHub Actions**: CI/CD workflow automation
- **Python 3.11**: Runtime environment
- **Regex**: Number extraction from HTML
