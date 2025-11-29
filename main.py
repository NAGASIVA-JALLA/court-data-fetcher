import sys
import asyncio
import re

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
from models import CourtQuery
from scraper import fetch_case_details


# ------------------ CLEAN TEXT FUNCTION ------------------
def clean_text(v):
    if not v:
        return ""
    v = v.replace("\u00a0", " ")
    v = (
        v.encode("latin-1", "ignore")
         .decode("utf-8", "ignore")
         .encode("ascii", "ignore")
         .decode()
    )
    return v.strip()


# ------------------ DB INIT ------------------
Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# ------------------ DB SESSION ------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------ UPDATED EXTRACT FUNCTION ------------------
def extract_info_from_table(table_data):
    # CASE 1 → table is empty or "No data available in table"
    if not table_data or (
        len(table_data) == 1 and
        list(table_data[0].values())[0].strip().lower() == "no data available in table"
    ):
        return "No data available", "No data available", "No data available"

    # CASE 2 → normal data exists
    first_row = table_data[0]

    diary_no_status = first_row.get("Diary No. / Case No.[STATUS]", "")
    petitioner_vs_respondent = first_row.get("Petitioner Vs. Respondent", "")
    listing_date_court_no = first_row.get("Listing Date / Court No.", "")

    diary_no_status = clean_text(diary_no_status)
    petitioner_vs_respondent = clean_text(petitioner_vs_respondent)
    listing_date_court_no = clean_text(listing_date_court_no)

    return diary_no_status, petitioner_vs_respondent, listing_date_court_no


# ------------------ ROUTES ------------------

@app.get("/form", response_class=HTMLResponse)
def form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.get("/test", response_class=HTMLResponse)
def test_template(request: Request):
    return templates.TemplateResponse("results.html", {"request": request, "result": {"case_table": []}})


@app.get("/saved-cases")
def get_saved_cases(db: Session = Depends(get_db)):
    cases = db.query(CourtQuery).order_by(CourtQuery.id.desc()).limit(10).all()
    return JSONResponse(content=[{
        "id": case.id,
        "case_type": case.case_type,
        "case_number": case.case_number,
        "case_year": case.case_year,
        "parties": case.parties,
        "next_hearing_date": case.next_hearing_date,
        "raw_html": case.raw_html,
    } for case in cases])


@app.post("/result", response_class=HTMLResponse)
def result(
        request: Request,
        case_type: str = Form(...),
        case_number: str = Form(...),
        case_year: str = Form(...),
        db: Session = Depends(get_db)
):
    result_data = fetch_case_details(case_type, case_number, case_year)

    case_table = result_data.get("case_table", [])
    diary_no_status, petitioner_vs_respondent, listing_date_court_no = extract_info_from_table(case_table)

    query = CourtQuery(
        case_type=case_type,
        case_number=case_number,
        case_year=case_year,

        # 🔥 UPDATED FIELD NAME HERE
        Diary_No_Case_No_Status=diary_no_status,

        petitioner_vs_respondent=petitioner_vs_respondent,
        listing_date_court_no=listing_date_court_no,
    )

    db.add(query)
    db.commit()
    db.refresh(query)

    return templates.TemplateResponse("results.html", {
        "request": request,
        "result": result_data
    })
