from playwright.sync_api import sync_playwright

print("Scraper Function Started")

# CLEANING FUNCTION TO REMOVE ALL BAD CHARACTERS
def clean_text(value):
    if not value:
        return ""

    # Remove non-breaking spaces
    value = value.replace("\u00a0", " ")

    # Remove weird hidden unicode
    value = (
        value.encode("latin-1", "ignore")
        .decode("utf-8", "ignore")
        .encode("ascii", "ignore")
        .decode()
    )

    # Remove extra spaces
    return value.strip()


def fetch_case_details(case_type, case_number, case_year):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://delhihighcourt.nic.in/app/get-case-type-status")

        page.wait_for_selector("#case_type", timeout=10000)

        page.select_option("#case_type", value=case_type)
        page.fill("#case_number", case_number)
        page.select_option("#case_year", value=case_year)

        print("Please solve CAPTCHA manually...")
        input("After submitting CAPTCHA, press Enter here to continue...")

        page.wait_for_selector("#caseTable", timeout=120000)

        # Extract rows
        rows = page.query_selector_all("#caseTable tr")

        # Extract headers
        headers = [
            clean_text(cell.inner_text().strip())
            for cell in rows[0].query_selector_all("th")
        ]

        table_data = []

        # Detect "No data available"
        first_data_row = rows[1].query_selector_all("td")
        if len(first_data_row) == 1:
            return {"headers": headers, "case_table": []}

        # Extract table rows
        for row in rows[1:]:
            cells = [
                clean_text(cell.inner_text().strip())
                for cell in row.query_selector_all("td")
            ]
            if cells:
                table_data.append(dict(zip(headers, cells)))

        browser.close()

        return {
            "headers": headers,
            "case_table": table_data
        }
