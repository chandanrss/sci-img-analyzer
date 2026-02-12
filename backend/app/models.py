from sqlalchemy import Column, Integer, Float, String
from app.database import Base

class ImageAnalysis(Base):
    __tablename__ = "image_analysis"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    total_objects = Column(Integer)
    average_area = Column(Float)
