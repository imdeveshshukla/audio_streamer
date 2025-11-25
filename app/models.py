from sqlalchemy import Column, Integer, String, BigInteger
from app.database import Base

class Clip(Base):
    __tablename__ = "clips"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    genre = Column(String)
    duration = Column(String)
    audio_url = Column(String, nullable=False)
    play_count = Column(BigInteger, default=0)
