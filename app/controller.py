from sqlalchemy.orm import Session
from app.models import Clip
from sqlalchemy import update

def get_all_clips(db: Session):
    return db.query(Clip).all()
  
def get_clip(db: Session, clip_id: int):
  return db.query(Clip).filter(Clip.id == clip_id).first()

def increment_play_count(db: Session, clip_id: int):
    stmt = (
        update(Clip)
        .where(Clip.id == clip_id)
        .values(play_count=Clip.play_count + 1)
    )
    db.execute(stmt)
    db.commit()
    
def create_clip(db: Session, clip_data):
    new_clip = Clip(
        title=clip_data.title,
        description=clip_data.description,
        genre=clip_data.genre,
        duration=clip_data.duration,
        audio_url=clip_data.audio_url,
        play_count=0
    )
    db.add(new_clip)
    db.commit()
    db.refresh(new_clip)
    return new_clip