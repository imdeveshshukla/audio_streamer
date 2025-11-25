from pydantic import BaseModel

class ClipBase(BaseModel):
    id: int
    title: str
    description: str | None = None
    genre: str | None = None
    duration: str | None = None
    audio_url: str

    class Config:
        orm_mode = True
        
class ClipStats(BaseModel):
    play_count: int
    title: str
    description: str | None = None
    genre: str | None = None
    duration: str | None = None
    
    class Config:
        orm_mode = True