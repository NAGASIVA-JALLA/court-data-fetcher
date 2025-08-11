from playwright.sync_api import sync_playwright

def fetch_case_details(case_type, case_number, case_year):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://delhihighcourt.nic.in/app/get-case-type-status")

        # Wait for dropdown
        page.wait_for_selector("#case_type", timeout=10000)

        # Fill the fields
        page.select_option("#case_type", value=case_type)
        page.fill("#case_number", case_number)
        page.select_option("#case_year", value=case_year)

        print("Please solve the CAPTCHA and submit manually in the opened browser...")
        input("After submitting CAPTCHA, press Enter here to continue scraping...")

        # Wait for result element to appear (adjust selector based on actual result HTML)
        page.wait_for_selector("#caseTable", timeout=120000)  # 2 minutes to solve CAPTCHA

        # Extract all rows and columns into a list of dicts
        rows = page.query_selector_all("#caseTable tr")
        table_data = []

        # Assuming first row is header
        headers = [cell.inner_text().strip() for cell in rows[0].query_selector_all("th")]
        #EXACT ROWS
        for row in rows[1:]:
            cells = [cell.inner_text().strip() for cell in row.query_selector_all("td")]
            if cells:
                table_data.append(dict(zip(headers, cells)))

        data = {
            "case_table": table_data
        }

        browser.close()
        return data
