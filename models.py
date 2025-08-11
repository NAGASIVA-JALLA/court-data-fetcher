from sqlalchemy import Column, Integer, String, Text
from database import Base

class CourtQuery(Base):
    __tablename__ = "court_queries"

    id = Column(Integer, primary_key=True, index=True)
    case_type = Column(String, index=True)
    case_number = Column(String)
    case_year = Column(String)

    diary_no_status = Column(String)           # <-- new field
    petitioner_vs_respondent = Column(String)  # <-- new field
    listing_date_court_no = Column(String)    # <-- new field


