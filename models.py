from sqlalchemy import Column, Integer, String, Text
from database import Base

class CourtQuery(Base):
    __tablename__ = "court_queries"

    id = Column(Integer, primary_key=True, index=True)
    case_type = Column(String, index=True)
    case_number = Column(String)
    case_year = Column(String)

    Diary_No_Case_No_Status = Column(String)
    petitioner_vs_respondent = Column(String)  
    listing_date_court_no = Column(String)    


