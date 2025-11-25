from sqlalchemy.orm import Session
from app.models import Clip


def get_all_clips(db: Session):
    return db.query(Clip).all()
  
def get_clip(db: Session, clip_id: int):
  return db.query(Clip).filter(Clip.id == clip_id).first()