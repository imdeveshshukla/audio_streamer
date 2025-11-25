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