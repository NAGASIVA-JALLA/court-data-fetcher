# Court-Data Fetcher & Mini-Dashboard (Delhi High Court Scraper)

A technical assignment completed for Indrachala

## 📌 About This Project

This project was developed as part of a technical assignment from Indrachala.  
The task required building a mini web app capable of:

➡️ Fetching public case information from an official Indian court website  
➡️ Handling manual CAPTCHA legally  
➡️ Saving results in a PostgreSQL database  
➡️ Displaying the case information in a clean, simple HTML dashboard  

The official assignment title was:

**Task 1 — “Court-Data Fetcher & Mini-Dashboard”**

For this assignment, I selected the Delhi High Court website:  
👉 https://delhihighcourt.nic.in/

It is stable, public, structured, and ideal for scraping with Playwright.

---

## 🚀 What This Project Demonstrates

✔ FastAPI backend development  
✔ Web scraping using Playwright  
✔ Manual CAPTCHA handling (legal and required)  
✔ HTML form-based frontend for case search  
✔ PostgreSQL database integration  
✔ Clean result rendering  
✔ Storing raw HTML + search history  

---

## ⚙️ How the System Works (Simple Flow)

User opens the web app at:  
http://127.0.0.1:8000/form  

User fills in the case details (type, number, year).  

Playwright launches a browser automatically.  

The scraper autofills the official Delhi High Court search form.  

Browser waits for the user to solve CAPTCHA manually.  

User submits the form on the website.  

User presses Enter in the terminal to continue.  

Scraper extracts:  
- Parties’ names  
- Case status  
- Next/Last hearing date  

Data is:  
- Shown on the results HTML page  
- Stored in PostgreSQL  

---

## ⭐ Features

### 🔹 Web Application Features
- Clean HTML form for entering case details  
- Auto-navigation and auto-filling of court form  
- Manual CAPTCHA step → ensures legal scraping  
- Stores:  
  - Search parameters  
  - Extracted case details  
  - Raw HTML page  

### 🔹 Scraped Case Details
- Petitioner vs Respondent  
- Next hearing date (or last hearing if next is unavailable)  
- Case status  
- Diary number information  

### 🔹 Database Storage
Every search entry is saved in PostgreSQL using SQLAlchemy ORM.

---

## 🧠 Technical Stack

Component | Technology  
--------- | ----------  
Backend Framework | FastAPI  
Scraper | Playwright  
Database | PostgreSQL  
ORM | SQLAlchemy  
Templates | Jinja2  
Async Support | async SQLAlchemy + async Playwright  
Frontend | HTML + Jinja templates  

---

## 🛑 CAPTCHA Handling (Important)

CAPTCHA is not bypassed (as that is illegal and violates terms).  
Instead, this system uses:

✔ Playwright browser opens visibly  
✔ User manually enters CAPTCHA  
✔ Scraper continues after confirmation in terminal  

This approach is safe, legal, and recommended.

---

## 📤 Data Extraction Details

The scraper reliably extracts:

- Parties’ Names  
- Next Hearing Date (or Last Date)  
- Case Status  
- Diary Number & Listing Info  

---

## ⚠️ Limitations (From Court Website Itself)

- Filing Date is not available on search results page  
- Order/Judgment PDF links are not provided  
- To fetch PDFs, deeper scraping into case-detail pages is required  

---

## 🗂️ Database Schema

**Table: court_queries**

Column | Type | Description  
-------|------|-------------  
id | Integer | Primary key  
case_type | String | e.g., W.P.(C), BAIL  
case_number | String | Case number  
case_year | String | Year of filing  
diary_no_status | String | Diary number + case status  
petitioner_vs_respondent | String | Parties involved  
listing_date_court_no | String | Next/Last listing date  

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the repository
git clone https://github.com/NAGASIVA-JALLA/court-data-fetcher.git  
cd court-data-fetcher  

### 2️⃣ Create a virtual environment
python -m venv venv  
venv\Scripts\activate   # Windows  
source venv/bin/activate  # Mac/Linux  

### 3️⃣ Install dependencies
pip install -r requirements.txt  

### 4️⃣ Install Playwright browsers
playwright install  

### 5️⃣ Configure PostgreSQL

Create a database:  
court_data  

Update your .env file:  
DATABASE_URL=postgresql://username:password@localhost:5432/court_data  

### 6️⃣ Run FastAPI
uvicorn main:app --reload  

### 7️⃣ Open the app
👉 http://127.0.0.1:8000/form  

---

## 🖥️ How to Use

Enter case type, number, and year  
Submit the form  
Playwright opens Delhi High Court website  
Solve CAPTCHA manually  
Submit the court form  
Return to terminal and press Enter  
View results on the frontend  
Data is automatically saved in PostgreSQL  

---

## 🚧 Future Improvements

- Automate CAPTCHA if legally permitted  
- Add case-order/judgment PDF scraper  
- Create complete dashboard with charts  
- Add user login system  
- Error reporting + logs page  

---

## 📸 Screenshots


### 📝 Form Page  
![Form Page](screenshots/form_page.png)

### 📄 Result Page  
![Result Page](screenshots/result_page.png)

### 🗄️ Database View  
![Database View](screenshots/database_view.png)

---

## 🙌 Thank You!

👩‍💻 **Developed by:** NAGASIVA JALLA  
GitHub: https://github.com/NAGASIVA-JALLA ([NAGASIVA JALLA](https://github.com/NAGASIVA-JALLA)
